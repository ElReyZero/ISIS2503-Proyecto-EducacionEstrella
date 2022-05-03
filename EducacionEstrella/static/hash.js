import createHash from './crypto.js'
function setHash()
{
    var string = document.getElementById("estudiante").value + document.getElementById("analista").value + String(document.getElementById("montoAPagar").value) + document.getElementById("fechaSolicitud").value + document.getElementById("fechaAprobacion").value;
    document.getElementById("hash").value = createHash('sha256').update(string).digest('hex');
};

document.getElementById("submitButton").addEventListener("click", setHash());
