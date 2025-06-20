from flask import Flask, redirect, url_for, flash, render_template, session # Session for saving session vars
import imageio.v3 as iio # Image processing thing
import os
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from forms import UploadForm # Le upload form
from werkzeug.utils import secure_filename # Use this later to get safe files and stuff
from collections import Counter # Use later to track colors in img

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
bootstrap = Bootstrap5(app) # Get bootstrap 5 for the app

IMG_FOLDER = 'static/assets/user_imgs' # Folder for computer to store images later

def rgb_to_hex(rgb):
    # Format the 3 numbers as two digit LOWERCASE hexadecimal numbers, with padding if needed (0a instead of a)
    # Add the hashtag in front for easier use in html
    return '#{:02x}{:02x}{:02x}'.format(*rgb) # Asterisk formats each number in tuple individually but returns combined
                                                                                                            # hex code

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/img-upload', methods=['GET', 'POST'])
def img_upload():
    form = UploadForm() # render the form
    if form.validate_on_submit(): # If a POST request is made
        image_data = form.image_file.data # Get the image (fileobj from form)
        img_name = secure_filename(image_data.filename) # Save the img name as a variable
        save_path = os.path.join(IMG_FOLDER, img_name) # Combine the IMG folder path with the img name path
        image_data.save(save_path) # Now save the image imported in the img folder

        # Store the image name/path in the session to be accessed later
        session['last_uploaded'] = img_name

        return redirect(url_for('color_results'))

    return render_template('img_upload.html', form=form)

@app.route('/img-color-results')
def color_results():
    image_name = session.get('last_uploaded')
    if not image_name: # If there was no image name return an error
        flash("Error getting image.", 'danger')
        return redirect(url_for('img_upload'))

    img_path = os.path.join(IMG_FOLDER, image_name) # join the paths again, but this time for IIO reading
    # load into num py array. Shape is height, width, channels, channels can be 3 for RGB, or 4 if RGB + Alpha
    # (transparent)
    image_array = iio.imread(img_path)
    # If the image has an alpha section/is transparent, drop it
    if image_array.shape[-1] == 4:
        image_array = image_array[:, :, :3]

    # Flatten and count, make one big list of RGB values instead of a 2d array
    pixels = image_array.reshape(-1, 3)
    pixel_tuples = []
    for pixel in pixels:
        pixel_tuple = tuple(pixel) # Convert the little RGB list with 3 elements to a tuple [255, 0, 3] >> (255, 0, 3)
        pixel_tuples.append(pixel_tuple)
    color_counts = Counter(pixel_tuples) # Counts the instances of every unique item by default, returns dict
    most_prevalent = color_counts.most_common(12) # Get the 12 most prevalent colors in the dictionary (or tuples of rgb)

    # Now get the list of hex colors with counts, make tuple and append to list
    hex_colors_w_cnt = []
    for color_n_count in most_prevalent:
        color = color_n_count[0]
        count = color_n_count[1]
        hex_code = rgb_to_hex(color)
        hex_code_count_tuple = (hex_code, count)
        hex_colors_w_cnt.append(hex_code_count_tuple)
    # Make a list of numbers for every index in the tuples list. Add 1 to LENGTH, because range won't include the last num, so you want it.
    num_list = list(range(1, len(hex_colors_w_cnt) + 1))
    zipped = list(zip(hex_colors_w_cnt, num_list))
    # Return the ZIPPED list with our hex colors and count tuples and the number of them we have, in HUMAN COUNT from 1
    return render_template('color_results.html', zipped=zipped,
                           img_path=img_path)

if __name__ == "__main__":
    app.run(debug=True)