import axios from "axios"
const instance =axios.create({
    baseURL:'http://192.168.20.42:5000',
    timeout:1000,
    // headers:{
    //     "Content-type":"application/json"
    // }
});
export default instance;