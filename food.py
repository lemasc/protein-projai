from typing import TypedDict, Literal
import pandas as pd
import random
import time

df = None
url = 'https://docs.google.com/spreadsheets/d/1_9AZb7hF7494ZyhKx-bTCcLHByKm0uXBq_pBInU1E84/export?gid=191160001&format=csv'
fetch_at = 0


def split_to_list(string):
    return [x.strip() for x in string.split(",")]


def get_df(use_cached=True):
    global df, fetch_at
    if use_cached and df is not None:
        return df
    df = pd.read_csv(url, converters={"ingredients": split_to_list})
    fetch_at = time.time()
    return df


class FoodData(TypedDict):
    menu: str
    type: Literal["main", "dessert"]
    ingredients: list[str]
    protein_per_serving: float

# สุ่มรายการอาหาร 1 รายการ จาก list ทั้งหมด


def get_random_food(food_type):
    df = get_df()
    # สุ่ม index ในช่วงที่ต้องการ
    dest = df[df["type"] == food_type]
    random_index = random.randint(0, dest.shape[0] - 1)
    data_at_index = dest.iloc[random_index]
    data_dict: FoodData = data_at_index.to_dict()
    return data_dict


def calculate_protein_from_disease(disease):
    min_protein = 1
    max_protein = 1
    if disease == "ไตวายเรื้อรัง":
        min_protein = 0.6
        max_protein = 0.6
    elif disease in ("ตับ", "มะเร็ง", "ไฟไหม้กดทับ"):
        min_protein = 1.2
        max_protein = 2

    return min_protein, max_protein


def calculate_protein_from_age(age):
    min_protein = 1
    max_protein = 1
    if age < 1:
        min_protein = 1.56
        max_protein = 1.56
    elif age <= 18:
        min_protein = 1.05
        max_protein = 1.2
    elif age >= 60:
        min_protein = 1
        max_protein = 1.2

    return min_protein, max_protein


def calculate_protein(weight, age, activity=None, disease=None):
    min_protein, max_protein = calculate_protein_from_disease(disease)
    if min_protein == 1 and max_protein == 1:
        min_protein, max_protein = calculate_protein_from_age(age)

    if activity == "ออกกำลังกาย":
        min_protein += 0.4
        max_protein += 0.8
    elif activity == "นักเพาะกาย":
        min_protein += 0.8
        max_protein += 1.2
    elif activity == "ลดน้ำหนัก":
        min_protein -= 0.2
        max_protein -= 0.2
    else:
        min_protein += 0.1
        max_protein += 0.4

    # multiple by weight
    min_protein *= weight
    max_protein *= weight

    return min_protein, max_protein


def random_food_in_range(min_protein, max_protein, allergy=None):
    recommend_menu: list[FoodData] = []
    menu_names = set()
    total_protein = 0
    current_type = "main"
    random_attempt = 0
    while total_protein < min_protein and random_attempt < 2:
        random_attempt += 1
        random_food = get_random_food(current_type)
        menu_name = random_food["menu"]
        if allergy and allergy in "".join(random_food["ingredients"]):
            continue
        total_after_add = total_protein + random_food["protein_per_serving"]
        if not menu_name in menu_names and total_after_add <= max_protein:
            recommend_menu.append(random_food)
            menu_names.add(menu_name)
            total_protein = total_after_add
            random_attempt = 0
            if current_type == "main":
                current_type = "dessert"
            else:
                current_type = "main"
    return recommend_menu
