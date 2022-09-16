import axios from "axios"
var instance = axios.create(
    {
        headers:{
            "Content-type":"application/json"
        },
        baseURL:"http://192.168.20.42:5000/"
    }
)
export default instance