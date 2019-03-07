
class CreatePatient(FormView):
	model = PatientD
	form_class = PatientDForm
	success_url ="/entries/home/"
	template_name = "entries/create_p.html"

	def form_valid(self, form):
		form.save()
		return super(CreatePatient, self).form_valid(form)
