
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators, SubmitField, DecimalField, IntegerField
import json
import analyze_text


# Create app
app = Flask(__name__)


class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = TextAreaField("Enter Text:", validators=[
                     validators.InputRequired()])
    
    submit = SubmitField("Enter")

   
# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form = ReusableForm(request.form)
    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        p=analyze_text.main(seed)
        
        return render_template('main.html', input=[seed,p])
        
    # Send template information to index.html
    return render_template('index.html', form=form)


if __name__ == "__main__":
    # Run app
    app.run(host="0.0.0.0", port=80) 


