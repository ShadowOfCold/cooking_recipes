from django.contrib import admin
from .models import Category, Subcategory, Recipe, RecipeIngredient, RecipeImage, Comment, FavoriteRecipe, Tag, RecipeTag

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subcategory', 'created_at', 'difficulty')
    list_filter = ('user', 'subcategory', 'difficulty', 'created_at')
    search_fields = ('title', 'description', 'ingredients')
    ordering = ('-created_at',)
    inlines = [RecipeIngredientInline, RecipeImageInline]
    readonly_fields = ('created_at', 'updated_at') # Поля только для чтения

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'text', 'rating', 'created_at')
    list_filter = ('user', 'recipe', 'rating', 'created_at')
    search_fields = ('text', 'user__username', 'recipe__title') # Поиск по связанным полям
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__title')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Tag, TagAdmin)
