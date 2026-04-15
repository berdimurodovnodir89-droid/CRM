import { useEffect,useState } from "react"
import api from "../api/api"

export default function Leads(){

  const [leads,setLeads] = useState([])

  useEffect(()=>{

    api.get("/leads")
      .then(res=>{
        setLeads(res.data.data)
      })

  },[])

  return(

    <div style={{padding:40}}>

      <h2>Leads</h2>

      {leads.map(l=>(
        <div key={l.id}>

          {l.name} - {l.phone}

        </div>
      ))}

    </div>

  )

}