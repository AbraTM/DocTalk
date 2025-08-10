"use client"

import React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Loading from "./Loading";
import styles from "./SignUpForm.module.css";
import { createUser, loginUser, signUpWithGoogle } from "@/utils/firebaseAuth";

export default function SignUpForm(){
    // Handle user redirect and auth check
    const { user, loading } = useAuth()
    const router = useRouter()

    React.useEffect(() => {
        if(!loading && user){
            router.replace("/upload")
        }
    }, [loading, user, router])

    const [isLogin, setIsLogin] = React.useState(false);
    const [userInput, setUserInput] = React.useState({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: "",
    })
    const [errorMsg, setErrorMsg] = React.useState("");

    const handleModeSwitch = () => {
        setErrorMsg("");
        setIsLogin(prev => !prev)
    }

    const handleChange = (event) => {
        const {name, value} = event.target;
        setUserInput((prev) => {
            return{
                ...prev,
                [name] : value
            }
        });
    }

    const handleGoogleLogin = async () => {
        const { user, error } = await signUpWithGoogle();
        if(error){
            console.log(error)
            setErrorMsg(error.message)
            return;
        }
    }
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        if(!isLogin){
            // Validation
            if(!userInput.firstName){
                setErrorMsg("Please provide a first name.");
                return;
            }
            if(!userInput.lastName){
                setErrorMsg("Please provide a last name.");
                return;
            }

            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if(!userInput.email){
                setErrorMsg("Please provide an email.");
                return;
            }else if(!emailRegex.test(userInput.email)){
                setErrorMsg("Please provide a valid email.");
                return;
            }
            if(!userInput.password){
                setErrorMsg("Please provide a password.");
                return;
            }
            if(userInput.confirmPassword !== userInput.password){
                setErrorMsg("Password doesn't match.");
                return;
            }

            setErrorMsg("");
            console.log("Form submitted!!")
            const { user, error } = await createUser(userInput);
            if (error) {
                console.log(error.code);

                switch (error.code) {
                    case "auth/email-already-in-use":
                        setErrorMsg("An account with this email already exists.");
                        break;
                    default:
                        setErrorMsg("Something went wrong. Please try again.");
                }
                return;
            }
            setErrorMsg("");
            console.log(user);

        }else{
            // Validation
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if(!userInput.email){
                setErrorMsg("Please provide an email.");
                return;
            }else if(!emailRegex.test(userInput.email)){
                setErrorMsg("Please provide a valid email.");
                return;
            }
            if(!userInput.password){
                setErrorMsg("Please provide a password.");
                return;
            }

            setErrorMsg("");
            console.log("Form submitted!!");
            const { user, error } = await loginUser(userInput);
            if (error) {
                console.log(error.code);

                switch (error.code) {
                    case "auth/email-already-in-use":
                        setErrorMsg("An account with this email already exists.");
                        break;
                    default:
                        setErrorMsg("Something went wrong. Please try again.");
                }
                return;
            }
            setErrorMsg("");
            console.log(user);
        }
    }

    if(loading || user){
        return <Loading />
    }
    return(
        <div className={styles.signupFormCn}>
            <h3>{isLogin ? 'Login' : 'Create an account'}</h3>
            {
                !isLogin
                ?
                <form className={styles.signupForm} onSubmit={handleSubmit}>
                    <label htmlFor="firstName">First Name</label>
                    <input type="text" id="firstName" name="firstName" placeholder="Mads" value={userInput.firstName} onChange={handleChange}></input>

                    <label htmlFor="lastName">Last Name</label>
                    <input type="text" id="lastName" name="lastName" placeholder="Micheals" value={userInput.lastName} onChange={handleChange}></input>

                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="madsMich199@gmail.com" value={userInput.email} onChange={handleChange}></input>

                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="bananafish" value={userInput.password} onChange={handleChange}></input>

                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <input type="password" id="confirmPassword" name="confirmPassword" placeholder="bananafish" value={userInput.confirmPassword} onChange={handleChange}></input>
                    <div className={styles.errorMsg}>
                        <p
                            style={{
                                opacity: errorMsg ? "1" : "0",
                                visibility: errorMsg ? "visible" : "hidden",
                                minHeight: "1.5rem",
                                transition: "opacity 0.2s ease"
                            }}
                        >
                            {errorMsg || ""}
                        </p>
                    </div>
                    <button type="submit" className={styles.signUpButton}>Create an account</button>
                </form>
                :
                <form className={styles.signupForm} onSubmit={handleSubmit}>
                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="madsMich199@gmail.com" value={userInput.email} onChange={handleChange}></input>

                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="bananafish"  value={userInput.password} onChange={handleChange}></input>
                    <div className={styles.errorMsg}>
                        <p
                            style={{
                                opacity: errorMsg ? "1" : "0",
                                visibility: errorMsg ? "visible" : "hidden",
                                minHeight: "1rem",
                                transition: "opacity 0.2s ease"
                            }}
                        >
                            {errorMsg || ""}
                        </p>
                    </div>
                    <button type="submit" className={styles.signUpButton}>Login</button>
                </form>
            }
            <div className={styles.orLineCn}>
                <div className={styles.orLine}></div>
                <div>Or</div>
                <div className={styles.orLine}></div>
            </div>
            <div className={styles.otherSignup} onClick={handleGoogleLogin}>
                <p>Sign in with these.</p>
                <button className={styles.googleLogin}>
                    <img src="/google.png"></img>
                </button>
            </div>
            <div className={styles.switchMode}>
                <div>{isLogin ? "Don't have an account? " : "Already signed up? "}<a onClick={handleModeSwitch}>{!isLogin ? "Login" : "Sign Up"}</a></div>
            </div>
        </div>
    )
}