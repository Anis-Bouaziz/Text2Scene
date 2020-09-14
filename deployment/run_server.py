
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators, SubmitField, DecimalField, IntegerField
import json
import text_analysis
from waitress import serve

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
        lang=request.form['lang']
        
        p=text_analysis.main(seed,lang)
        
        return render_template('main.html', input=[seed,p])
        
    # Send template information to index.html
    return render_template('index.html', form=form)

@app.errorhandler(500)
def server_error(e):
    form = ReusableForm(request.form)
    return render_template('index.html', form=form), 500
@app.errorhandler(404)
def page_not_found(e):
    form = ReusableForm(request.form)
    return render_template('index.html', form=form), 404

if __name__ == "__main__":
    # Run app
    app.run(host="0.0.0.0", port=80) 
 
    #serve(app, host='0.0.0.0', port=8080)


