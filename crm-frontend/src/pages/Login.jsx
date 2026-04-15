import { useState } from "react"
import api from "../api/api"

export default function Login(){

  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")

  const login = async () => {

    try{

      const res = await api.post("/auth/login",{
        email,
        password
      })

      const token = res.data.access_token || res.data.data?.access_token

      localStorage.setItem("token",token)

      window.location.href="/dashboard"

    }catch{
      alert("Login failed")
    }

  }

  return(

    <div style={{padding:40}}>

      <h2>CRM Login</h2>

      <input
        placeholder="Email"
        onChange={e=>setEmail(e.target.value)}
      />

      <br/><br/>

      <input
        type="password"
        placeholder="Password"
        onChange={e=>setPassword(e.target.value)}
      />

      <br/><br/>

      <button onClick={login}>
        Login
      </button>

    </div>

  )

}