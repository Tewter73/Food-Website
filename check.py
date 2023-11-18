def load_tags(category):
    global conn, cursor
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    tag_columns = []

    if category == 'savory':
        tag_columns = ["chili", "rice", "meat", "shrimp_paste", "noodle", "soup", "pickled_fish", "one_dish_meal", "fried", "stir_fried"]
    elif category == 'dessert':
        tag_columns = ["water", "fruit", "cold", "hot", "thai_dessert", "baked", "fried", "small_piece"]

    conn.close()

    return tag_columns

def show_selected_tag_food(category, selected_tags):
    st.title(f"เมนูอาหารที่มี Tags: {', '.join(selected_tags)}")
    food_data = load_food_data_with_nutrition(category)

    for food_id, food_name, kcal, protein, fat, carbohydrate, *tags in food_data:
        if set(selected_tags).intersection(set(tags)):
            st.write(food_name)
            show_image_and_nutrition(food_id, food_name, category)

print(f"Category: {category}")
print(f"Selected Tags: {selected_tags}")
print(f"Food Data: {food_data}")
