from flask import Flask, request, render_template, url_for, redirect, send_from_directory, make_response
from forms import UpdateForm, LiquidateForm, AddForm, FindPortForm
from editDB import addtoDB, removeDB, changeQuantity
from portfolio import getPortfolioValue, getStats, producePNG, getPortfolioComponents

MEDIA_FOLDER = "uploads"

app = Flask(__name__)
app.config['SECRET_KEY'] = '176a19ffa0d1b06300919c971c92a2ef'

@app.route("/portfolio/<portfolioComponents>/<portfolioStats>")
def display(portfolioComponents,portfolioStats):
	r = make_response(render_template('display.html', portfolioComponents=portfolioComponents, portfolioStats=portfolioStats))
	r = add_header(r)
	return r
	

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)


@app.route("/", methods=['GET','POST'])
def index():
	update_form = UpdateForm()
	liquidate_form = LiquidateForm()
	add_form = AddForm()
	find_port_form = FindPortForm()


	if find_port_form.SubmitFind_Port.data:
		try:
			dataframe = getPortfolioValue(find_port_form.Find_Portfolio.data, "database.xlsx")
			producePNG(dataframe, "uploads/image.png")
			portfolioComponents = getPortfolioComponents(find_port_form.Find_Portfolio.data, "database.xlsx")
			portfolioComponents = portfolioComponents.to_string()
			portfolioStats = getStats(dataframe)
			return redirect(url_for('display', portfolioStats=portfolioStats, portfolioComponents=portfolioComponents))
		except:
			print("ERROR EMAIL NOT IN DATABASE")

	if add_form.SubmitAdd.data:
		addtoDB(add_form.Add_Portfolio.data, add_form.Add_Ticker.data, float(add_form.Price.data), int(add_form.Quantity.data), "database.xlsx")

	if liquidate_form.SubmitLiquidate.data:
		removeDB(liquidate_form.Liquidate_Portfolio.data, liquidate_form.Liquidate_Ticker.data, "database.xlsx", "database.xlsx")
	
	if update_form.SubmitUpdate.data:
		changeQuantity(update_form.Update_Portfolio.data, update_form.Update_Ticker.data, int(update_form.New_Quantity.data), "database.xlsx", "database.xlsx")
	
	return render_template('index.html', add_form=add_form, liquidate_form=liquidate_form, update_form=update_form, find_port_form=find_port_form)

@app.after_request
def add_header(r):
    r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '-1'
    return r

if __name__ == '__main__':
	app.run(debug=True)
