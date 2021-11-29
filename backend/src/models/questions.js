const mongoose = require("mongoose");

const questionSchema = new mongoose.Schema(
	{
		
		author: {
			type: mongoose.Schema.Types.ObjectId,
			ref: "User",
		},

		image: {
			type: Buffer
		},
		modified_image:{
			type:Buffer
		}
	},
	{ timestamps: true }
);

const Questions = mongoose.model("Question", questionSchema);
module.exports = Questions;
