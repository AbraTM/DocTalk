import { auth, googleProvider } from "./firebaseConfig";
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, signInWithPopup, signOut } from "firebase/auth";

export const createUser = async (userData) => { 
    try{
        const userCredential = await createUserWithEmailAndPassword(auth, userData.email, userData.password);
        return {
            user: userCredential.user,
            error: null
        };
    }catch (error){
        return {
            user: null,
            error: error
        };
    }
} 

export const loginUser = async (userData) => {
    try{
        const userCredential = await signInWithEmailAndPassword(auth, userData.email, userData.password);
        return {
            user: userCredential.user,
            error: null
        };
    }catch (error){
        return {
            user: null,
            error: error
        };
    }
}

export const signUpWithGoogle = async () => {
    try {
        const userCredential = await signInWithPopup(auth, googleProvider);
        return {
            user: userCredential.user,
            error: null
        };
    }catch (error){
        return {
            user: null,
            error: error
        };
    }
}

export const logout = async () => {
    try{
        await signOut(auth)
        console.log("Logged Out.")
    } catch(error){
        console.error("Logout Failed.", error)
    }
}