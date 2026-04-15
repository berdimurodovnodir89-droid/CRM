import { useEffect,useState } from "react"
import api from "../api/api"

export default function Dashboard(){

  const [stats,setStats] = useState(null)

  useEffect(()=>{

    api.get("/analytics/dashboard")
      .then(res=>{

        setStats(res.data.data)

      })

  },[])

  if(!stats) return <div>Loading...</div>

  return(

    <div style={{padding:40}}>

      <h1>CRM Dashboard</h1>

      <p>Total leads: {stats.total_leads}</p>
      <p>New leads: {stats.new_leads}</p>
      <p>Clients: {stats.clients}</p>
      <p>Conversion: {stats.conversion_rate}%</p>

    </div>

  )

}