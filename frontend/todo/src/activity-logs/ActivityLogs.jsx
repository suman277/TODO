import React from 'react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ActivityList from './ActivityList'
import "./ActivityLogs.css"

const ActivityLogs = () => {
  const [datas, setData] = useState([])
  const token = localStorage.getItem("token")
  const userId = localStorage.getItem("userId")
  const navigate = useNavigate();
  const fetchLogs = (id) => {
    fetch("http://localhost:8000/user/log/" + id, {
      method: "GET",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      }
    })
      .then((res) => {
        if (res.status === 401) {
          navigate("/login")
        }
        if (!res.ok) {
          throw new Error("An internal Error Occured")
        }
        return res.json();
      })
      .then(data => {
        console.log(data);
        setData(Array.isArray(data) ? data : data.logs ?? [])
      })
  }
  useEffect(() => {
    if (userId) {
      fetchLogs(userId)
    }
  }, [userId])

  const handelRedirect = () =>{
    navigate(-1);
  }


  return (
    <>
      <div className='main-body'>
        <div className='header'>
          <button onClick={handelRedirect}>&lt;--</button>
        </div>
        <div className='main'>
        <div className='page-title'>Audit Logs</div>
        <div>
          {datas &&
            datas.map((item, index) => {
              return <ActivityList key={item.id} log={item} isLast={index === datas.length - 1} />
            })}
        </div>
        </div>
      </div>
    </>
  )
}

export default ActivityLogs