import axios from 'axios'

const API = axios.create({
    baseURL: 'https://disks-apply-sorts-colors.trycloudflare.com/api/',
    headers: {
        'Content-Type': 'application/json',
    },
})

export default API