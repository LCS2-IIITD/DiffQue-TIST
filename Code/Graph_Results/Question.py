class Question:
	def __init__(self, question_id, question_text, asker_id, best_answer_id):
		self.question_id = question_id
		self.question_text = question_text
		self.asker_id = asker_id
		self.best_answer_id = best_answer_id
		self.best_answer_user_id = None
		self.non_best_answer_user_ids = []
	def __eq__(self, other):
		return other.question_id == self.question_id
	def __hash__(self):
		return self.question_id