def generate_profile(age: int) -> str:
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"   


print("Hello!")
user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)  
current_year = 2025
current_age = current_year - birth_year

hobbies = []
while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    hobbies.append(hobby)

life_stage = generate_profile(current_age)

user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies
}

summary = (
    f"Profile Summary:\n"
    f"Name: {user_profile['name'].title()}\n"
    f"Age: {user_profile['age']}\n"
    f"Life Stage: {user_profile['stage']}\n"
)

if user_profile["hobbies"]:
    summary += (
    f"Favorite Hobbies ({len(user_profile['hobbies'])}):\n"
    + "\n".join([f"- {h.title()}" for h in user_profile["hobbies"]])
)
else:
    summary += "You didn't mention any hobbies"

print("\n" + summary)
