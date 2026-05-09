const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const Article = sequelize.define('Article', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    title: {
      type: DataTypes.STRING,
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    image: {
      type: DataTypes.STRING,
      defaultValue: null
    },
    authorId: {
      type: DataTypes.INTEGER,
      allowNull: false
    },
    authorName: DataTypes.STRING,
    category: {
      type: DataTypes.STRING,
      defaultValue: 'General'
    },
    views: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    published: {
      type: DataTypes.BOOLEAN,
      defaultValue: true
    }
  }, {
    timestamps: true,
    createdAt: 'createdAt',
    updatedAt: 'updatedAt'
  });

  return Article;
};
