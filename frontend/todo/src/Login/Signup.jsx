import React from 'react'
import { useState } from 'react'
import "./Signup.css"

const Signup = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: ""
  })

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }))
  }
  const handleSubmit = (e) => {
    e.preventDefault()
    console.log(formData);
  }
  return (
    <>
      <div className='wrapper'>
        <div className='header'>
          <h1 className='signup-text'>Signup</h1>
        </div>
        <form>
          <div className='form'>
            <div className='username'>
              <label className='label'>Username</label>
              <input className='inputs' name="username" value={formData.username} onChange={handleChange}></input>
            </div>
            <div className='username'>
              <label className='label'>Email</label>
              <input className='inputs' name="email" value={formData.email} onChange={handleChange}></input>
            </div>
            <div className='username'>
              <label className='label'>Password</label>
              <input className='inputs' name="password" value={formData.password} onChange={handleChange}></input>
            </div>
            <div>
              <button className='submit' type = "submit" onClick={handleSubmit}>Signup</button>
            </div>
          </div>
        </form >
      </div >
    </>
  )
}

export default Signup