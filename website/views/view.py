from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify  # type: ignore
from website.controllers.ingredientcontroller import IngredientController
from website.controllers.foodcontroller import FoodController
from website.controllers.exercisecontroller import ExerciseController
from website.controllers.usercontroller import UserController
from website.controllers.mealcontroller import MealController
import os
import uuid
views = Blueprint('views', __name__)

@views.route('/logExercise', methods = ['GET', 'POST'])
def logExercise():
    if request.method == 'POST':
        exercise = request.form.get('exercise')
        id = session["user"]["id"]
        exercise_controller = ExerciseController()
        exercises = exercise_controller.user_do_exercise(exercise,id)
        print(exercises)

        meal_controller = MealController()
        exercise_controller = ExerciseController()
        id = session["user"]["id"]
        meals = meal_controller.get_all_meal(id)
        exercises = exercise_controller.get_all_exercise_by_userid(id)

        return render_template("log.html", meals = meals, exercises = exercises)

@views.route('/logFood', methods = ['GET', 'POST'])
def logFood():
    if request.method == 'POST':
        meal_type = request.form.get('meal_type')
        food = request.form.get('food')
        amount = request.form.get('quantity')
        id = session["user"]["id"]
        meal_controller = MealController()
        meal_controller.insert_meal(id, meal_type, food, amount)

        meal_controller = MealController()
        exercise_controller = ExerciseController()
        id = session["user"]["id"]
        meals = meal_controller.get_all_meal(id)
        exercises = exercise_controller.get_all_exercise_by_userid(id)

        return render_template("log.html", meals = meals, exercises = exercises)


@views.route('/logs')
def historyview():
    meal_controller = MealController()
    exercise_controller = ExerciseController()
    id = session["user"]["id"]
    meals = meal_controller.get_all_meal(id)
    exercises = exercise_controller.get_all_exercise_by_userid(id)
    print(meals)
    print(exercises)
    return render_template("log.html", meals = meals, exercises = exercises)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

@views.route('/editUser', methods = ['GET', 'POST'])
def editUserProfile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        id = session["user"]["id"]
        user_controller = UserController()
        user_data = user_controller.update(name,email,age,gender,height,weight, id)
        session["user"] = user_data[0]
        food_controller = FoodController()
        foods = food_controller.get_foods()
        exercise_controller = ExerciseController()
        exercises = exercise_controller.get_exercises()
        meal_controller = MealController()
        meals = meal_controller.get_all_daily_intake(id)
        return render_template("home.html", user = user_data[0], foods = foods, exercises = exercises, meals = meals)

@views.route('/')
def home():
    if "user" in session:
        user = session["user"]
        id = session["user"]["id"]
        food_controller = FoodController()
        foods = food_controller.get_foods()
        exercise_controller = ExerciseController()
        exercises = exercise_controller.get_exercises()
        meal_controller = MealController()
        meals = meal_controller.get_all_daily_intake(id)
        return render_template("home.html", user = user, foods = foods, exercises = exercises, meals = meals)
    else: 
        return redirect(url_for('auth.login'))
    

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

@views.route('/exercise')
def exercisescreen():
    exercise_controller = ExerciseController()
    exercises = exercise_controller.get_exercises()

    return render_template("exercise.html", exercises = exercises)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   

@views.route('/food', methods = ['GET', 'POST'])
def foodscreen():
    if request.method == 'POST':
        print("phương thức post đến /food")
        UPLOAD_FOLDER = './uploads'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        name = request.form.get('name')
        desc = request.form.get('description')
        method = request.form.get('cooking_method')
        file = request.files['image']
        ingredient_list = request.form.getlist('ingredients[]')
        amount_list = request.form.getlist('weights[]')
        if file:
            print("vào đc lưu file")
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file_path = file_path.replace("\\", "/")
            file.save(file_path)
            print("file_path_in_view "+ file_path)
            
            print("check ", name)
            print("check ", ingredient_list)
            print("check ", amount_list)

            food_controller = FoodController()
            foods = food_controller.add_food(name, ingredient_list, amount_list, file_path, desc, method)


    food_controller = FoodController()
    foods = food_controller.get_foods()

    ingredient_controller = IngredientController()
    ingredients = ingredient_controller.get_ingredients()

    return render_template("food.html", foods = foods, ingredients = ingredients)
    
@views.route('/food_detail/<int:id>', methods = ['GET', 'POST'])
def food_detail(id):
    print("kiểm tra trên food có id là : ")
    print(id)
    food_controller = FoodController()
    ingredients = food_controller.get_ingredient_by_food_id(id)
    print("checkpoint <1>")
    food = food_controller.get_food_by_id(id)
    print("checkpoint <2>")
    nutrition = food_controller.get_nutrition_by_food_id(id)
    return render_template("food_detail.html",  food = food, ingredients = ingredients, nutrition_totals = nutrition)

@views.route('/food_detail/rate', methods=['POST'])
def rate_food():
    data = request.get_json()
    rating = data.get('rating')
    id = data.get('id')

    # Thực hiện xử lý đánh giá (ví dụ lưu vào database)
    if rating:
        print(f"Đánh giá nhận được: {rating} sao tại food {id}")
        # Thêm logic lưu vào database tại đây   
        food_controller = FoodController()
        food_controller.vote(id, rating)
        return jsonify({"message": "Đánh giá đã được ghi nhận"}), 200
    else:
        return jsonify({"error": "Không nhận được đánh giá"}), 400

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
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
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