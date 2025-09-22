import streamlit_authenticator as stauth

names = ["Fabrizio Di Sciorio", "Manuele Villani", "Francesco Salvatori", "Marco Enrico La Rosa"]
usernames = ["Fds", "Mv", "Fs", "MR"]
passwords = ["123", "456", "678", "8910"]

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    "task_app", "abcdef", cookie_expiry_days=1)
