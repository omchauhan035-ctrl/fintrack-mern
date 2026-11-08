const Category = require('../models/Category');

// @desc    Get categories for user (includes defaults)
// @route   GET /api/categories
exports.getCategories = async (req, res, next) => {
  try {
    const { type } = req.query;
    const query = { userId: req.user._id };
    if (type && type !== 'all') {
      query.$or = [{ type }, { type: 'both' }];
    }

    const categories = await Category.find(query).sort({ isDefault: -1, name: 1 });

    res.json({
      success: true,
      data: { categories },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Create custom category
// @route   POST /api/categories
exports.createCategory = async (req, res, next) => {
  try {
    const { name, type, color, icon } = req.body;

    const category = await Category.create({
      userId: req.user._id,
      name,
      type,
      color: color || '#6366f1',
      icon: icon || 'tag',
      isDefault: false,
    });

    res.status(201).json({
      success: true,
      data: { category },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Update category
// @route   PATCH /api/categories/:id
exports.updateCategory = async (req, res, next) => {
  try {
    const { name, type, color, icon } = req.body;
    const updates = {};

    if (name !== undefined) updates.name = name;
    if (type !== undefined) updates.type = type;
    if (color !== undefined) updates.color = color;
    if (icon !== undefined) updates.icon = icon;

    const category = await Category.findOneAndUpdate(
      { _id: req.params.id, userId: req.user._id },
      updates,
      { new: true, runValidators: true }
    );

    if (!category) {
      return res.status(404).json({
        success: false,
        message: 'Category not found.',
      });
    }

    res.json({
      success: true,
      data: { category },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Delete category
// @route   DELETE /api/categories/:id
exports.deleteCategory = async (req, res, next) => {
  try {
    const category = await Category.findOne({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!category) {
      return res.status(404).json({
        success: false,
        message: 'Category not found.',
      });
    }

    if (category.isDefault) {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete default categories.',
      });
    }

    await category.deleteOne();

    res.json({
      success: true,
      message: 'Category deleted successfully.',
    });
  } catch (error) {
    next(error);
  }
};
