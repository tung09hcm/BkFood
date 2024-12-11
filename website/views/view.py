from flask import Blueprint, render_template, session, redirect, url_for, request  # type: ignore
from website.controllers.ingredientcontroller import IngredientController
import os
views = Blueprint('views', __name__)


@views.route('/')
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html")
    else: 
        return redirect(url_for('auth.login'))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   
@views.route('/food', methods = ['GET', 'POST'])
def foodscreen():
    return render_template("home.html")
    
@views.route('/food_detail', methods = ['GET', 'POST'])
def food_detail():
    return render_template("home.html")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
@views.route('/ingredient', methods = ['GET', 'POST'])
def ingredientscreen():
    if request.method == 'POST':
        UPLOAD_FOLDER = './uploads'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        ingredient_name = request.form.get('name')
        file = request.files['image']
        calcium = request.form.get('calcium')
        calories = request.form.get('calories')
        carbohydrates = request.form.get('carbohydrates')
        fats = request.form.get('fats')
        fiber = request.form.get('fiber')
        iron = request.form.get('iron')
        potassium = request.form.get('potassium')
        protein = request.form.get('protein')
        vitaminA = request.form.get('vitamin-a')
        vitaminC = request.form.get('vitamin-c')
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file_path = file_path.replace("\\", "/")
            file.save(file_path)
            print("file_path "+ file_path)
            with open(file_path, 'rb') as f:
                response = supabase.storage.from_("ingredient").upload(
                    path=f"public/{file.filename}",  # Đường dẫn ảnh trong bucket
                    file=f,
                    file_options={
                        "cache-control": "3600",
                        "upsert": "false",
                    },
                )
                print("==============================")
                print("response: ")
                print(response)
                print("==============================")
                full_path = response.full_path
                print("Full Path:", full_path)

    ingredient_controller = IngredientController()
    ingredients = ingredient_controller.get_ingredients()
    return render_template("ingredient.html", ingredients = ingredients)
    
@views.route('/ingredient_detail/<int:id>', methods=['GET', 'POST'])
def ingredient_detail(id):
    ingredient_controller = IngredientController()
    ingredient = ingredient_controller.get_ingredient_by_id(id)
    nutrition = ingredient_controller.get_nutrition_by_ingre_id(id)
    return render_template("ingredient_detail.html", ingredient=ingredient, nutrition=nutrition)