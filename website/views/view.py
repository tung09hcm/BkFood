from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify  # type: ignore
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
        print("phương thức post đến /ingredient")

        UPLOAD_FOLDER = './uploads'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        name = request.form.get('name')
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
            print("vào đc lưu file")
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file_path = file_path.replace("\\", "/")
            file.save(file_path)
            print("file_path_in_view "+ file_path)
            ingredient_controller = IngredientController()
            ingredient_controller.add_ingredient(file_path,name,calcium, calories, carbohydrates, fats, fiber, iron, potassium, protein, vitaminA, vitaminC)

    ingredient_controller = IngredientController()
    ingredients = ingredient_controller.get_ingredients()
    return render_template("ingredient.html", ingredients = ingredients)
    
@views.route('/ingredient_detail/<int:id>', methods=['GET', 'POST'])
def ingredient_detail(id):
    ingredient_controller = IngredientController()
    ingredient = ingredient_controller.get_ingredient_by_id(id)
    nutrition = ingredient_controller.get_nutrition_by_ingre_id(id)
    return render_template("ingredient_detail.html", ingredient=ingredient, nutrition=nutrition)

@views.route('/ingredient_detail/rate', methods=['POST'])
def rate_ingredient():
    data = request.get_json()
    rating = data.get('rating')
    id = data.get('id')

    # Thực hiện xử lý đánh giá (ví dụ lưu vào database)
    if rating:
        print(f"Đánh giá nhận được: {rating} sao tại ingredient {id}")
        # Thêm logic lưu vào database tại đây   
        ingredient_controller = IngredientController()
        ingredient_controller.vote(id, rating)
        return jsonify({"message": "Đánh giá đã được ghi nhận"}), 200
    else:
        return jsonify({"error": "Không nhận được đánh giá"}), 400