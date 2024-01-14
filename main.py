import subprocess
import instaloader
from instaloader.exceptions import ProfileNotExistsException
import os
import random
import time
import getpass
import webbrowser

subprocess.run(["pip", "install", "instaloader"])

print("Instagram Followback Checker")
time.sleep(1)
print("This script uses Instaloader version 3.11.")
time.sleep(1)
print("The script also saves the session but does not send it anywhere.")
time.sleep(1)
print("If you are unsure, please close this script.")
time.sleep(1)
print("Created on January 14, 2024.")
time.sleep(2)

username = input("Enter your Instagram username: ")
password = getpass.getpass("Enter your Instagram password: ")

loader = instaloader.Instaloader()

def login():
    try:
        loader.context.login(user=username, passwd=password)
    except LoginRequiredException as e:
        print(f"Login failed: {e}")
        exit(1)

login()

user_profile = instaloader.Profile.from_username(loader.context, username)

with open("following.txt", "w") as file_following:
    for following in user_profile.get_followees():
        file_following.write(f"{following.username}\n")

with open("followers.txt", "w") as file_followers:
    for follower in user_profile.get_followers():
        file_followers.write(f"{follower.username}\n")

def check_non_mutual_following():
    with open("following.txt", "r") as following_file, open("followers.txt", "r") as followers_file:
        following_set = set(following_file.readlines())
        followers_set = set(followers_file.readlines())

        non_mutual_following = following_set - followers_set

        with open("non_mutual_following.txt", "w") as output_file:
            for user in non_mutual_following:
                print(user.strip(), file=output_file)

profile_pic_cache = {}

def is_profile_pic_downloaded(username):

    user_directory = f"{username}_profile_pics"
    if os.path.exists(user_directory):
        return any(f.endswith('_profile_pic.jpg') for f in os.listdir(user_directory))
    return False


def download_and_save_profile(username):
    try:
        user_directory = f"{username}_profile_pics"
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)
        if username in profile_pic_cache:
            profile_pic_url = profile_pic_cache[username]
        else:
            user_profile = instaloader.Profile.from_username(loader.context, username)
            profile_pic_url = user_profile.get_profile_pic_url()

            profile_pic_cache[username] = profile_pic_url

        if profile_pic_url is not None:
            if not is_profile_pic_downloaded(username):
                loader.download_profilepic(user_profile)

                timestamp_filename = max(
                    (f for f in os.listdir(username) if f.endswith('_profile_pic.jpg')),
                    key=lambda f: os.path.getmtime(os.path.join(username, f))
                )

                downloaded_filename = os.path.join(username, timestamp_filename)
                new_filename = f"{username}_profile_pic.jpg"

                counter = 1
                while os.path.exists(new_filename):
                    new_filename = f"{username}_profile_pic_{counter}.jpg"
                    counter += 1

                os.rename(downloaded_filename, new_filename)

            with open("saved_profiles.txt", "a") as saved_profiles_file:
                saved_profiles_file.write(f"{username} - {profile_pic_url}\n")
        else:
            print(f"Warning: No profile picture found for {username}")

    except ProfileNotExistsException:
        print(f"Warning: Profile {username} not found.")
        time.sleep(random.uniform(2, 10))

def create_html_file():
    print("Creating HTML FIle...")
    with open("non_mutual_following.txt", "r") as input_file, open("index.html", "w") as output_file:
        output_file.write("<html><head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'></head><body class='bg-gray-100'>\n")
        output_file.write("<div class='container mx-auto my-8 p-8 bg-white shadow-lg rounded-lg'>\n")
        output_file.write("<h1 class='text-3xl font-bold mb-6 text-center'>User berikut tidak followback kamu, haha kasian deh lu..</h1>\n")
        output_file.write("<ul class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>\n")

        for user_name in input_file.readlines():
            user_name = user_name.strip()

            if not os.path.exists("saved_profiles.txt"):
                open("saved_profiles.txt", "w").close()

            with open("saved_profiles.txt", "r") as saved_profiles_file:
                saved_profiles = saved_profiles_file.read()
                if f"{user_name} -" not in saved_profiles:
                    download_and_save_profile(user_name)

            profile_link = f"https://www.instagram.com/{user_name}/"
            output_file.write(f"<li class='mb-4'><img src='{user_name}_profile_pic.jpg' alt='Profile Pic' class='rounded-full h-16 w-16 mx-auto mb-2'><div class='text-center'><a href='{profile_link}' class='text-blue-500 font-semibold'>{user_name}</a></div></li>\n")

        output_file.write("</ul>\n")
        output_file.write("</div></body></html>\n")
def open_html_file():
    html_file_path = "index.html"
    webbrowser.open(html_file_path)
check_non_mutual_following()

create_html_file()
print("HTML Created.")
print("Check at index.html")
open_html_file()

if os.path.exists("saved_profiles.txt"):
    os.remove("saved_profiles.txt")
print("Removing unused file...")
from clear_folder import remove_folder
current_directory = os.getcwd()
remove_folder(current_directory)
print("Closing...")
time.sleep(3)
print("3")
time.sleep(2)
print("2")
time.sleep(2)
print("1")
time.sleep(1)