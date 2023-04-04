import React from 'react'
import { useRef, useState, useEffect, useContext } from "react"
import AuthContext from "../context/AuthProvider"

const Login = () => {
    const { setAuth } = useContext(AuthContext)
    
    const userRef = useRef()
    const errRef = useRef()

    const [user, setUser] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');


    useEffect(() => {
        userRef.current.focus()
    }, [])

    useEffect(() => {
        setErrMsg('')
    }, [user, pwd])

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log(user, pwd)
        setUser('')
        setPwd('')
    }

    return (
        <section className='login'>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"}>{errMsg}</p>
            <h1>Sign In</h1>
            <form onSubmit={handleSubmit}>
                <label>Username: </label>
                <input 
                    type="text" 
                    id="username" 
                    ref={userRef}
                    autoComplete='off'
                    onChange={(e) => setUser(e.target.value)}
                    value = {user}
                    required
                />
                <label>Password: </label>
                <input 
                    type="password" 
                    id="password" 
                    onChange={(e) => setPwd(e.target.value)}
                    value = {pwd}
                    required
                />
                <button>Sign In</button>
            </form>
        </section>
    )
}

export default Login