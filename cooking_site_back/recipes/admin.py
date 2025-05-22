from django.contrib import admin
from .models import Recipe, Category, Subcategory, Ingredient

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('title', 'subcategory', 'difficulty', 'is_published')
    list_filter = ('subcategory', 'difficulty', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Ingredient)