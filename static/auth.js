//sign up
const signUpForm = document.querySelector('#registrationform');
signUpForm.addEventListener('submit', (e) => {
  e.preventDefault();

  //get user info
  const name = signUpForm['name'].value;
  const email = signUpForm['email'].value;
  const password = signUpForm['password'].value;

  //signUp User
  auth.createUserWithEmailAndPassword(email, password).then(cred => {

  })
})