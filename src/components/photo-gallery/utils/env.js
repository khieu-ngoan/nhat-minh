export let IMAGE_URL="/NguyenKhieuNhatMinh";
export const dns = process.env.REACT_APP_HOSTS.split(',')

export const dnsRandom = function(file){
    let host = dns[Math.floor(Math.random()*dns.length)];
    return `${host}/${file}`
}
