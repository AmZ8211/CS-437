from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class FindPortForm(FlaskForm):
	Find_Portfolio = StringField(label='updateEmail',validators=[DataRequired(), Email()])
	SubmitFind_Port = SubmitField('submit')

class UpdateForm(FlaskForm):
	Update_Portfolio = StringField(label='updateEmail',validators=[DataRequired(), Email()])
	Update_Ticker = StringField(label='updateStock',validators=[DataRequired(), Length(max=5)])
	New_Quantity = IntegerField(label='enter new quantity', default=0, validators=[DataRequired()])
	SubmitUpdate = SubmitField('submit')

class LiquidateForm(FlaskForm):
	Liquidate_Portfolio = StringField(label='liquidateEmail',validators=[DataRequired(), Email()])
	Liquidate_Ticker = StringField(label='liquidateStock',validators=[DataRequired(), Length(max=5)])
	SubmitLiquidate = SubmitField('submit')

class AddForm(FlaskForm):
	Add_Portfolio = StringField(label='Email',validators=[DataRequired(), Email()])
	Add_Ticker = StringField(label='Stock',validators=[DataRequired(), Length(max=5)])
	Price = DecimalField(label='enter price', default=00.00, validators=[DataRequired()])
	Quantity = IntegerField(label='enter quantity', default=0, validators=[DataRequired()])
	SubmitAdd = SubmitField('submit')

