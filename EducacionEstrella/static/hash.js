var form = document.getElementById("post-form")
form.addEventListener("submit", async function() {
    var string = document.getElementById("id_estudiante").value + document.getElementById("id_analista").value + String(document.getElementById("id_montoAPagar").value) + document.getElementById("id_fechaAprobacion").value;
    const utf8 = new TextEncoder().encode(string);
    var hash = await crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray
          .map((bytes) => bytes.toString(16).padStart(2, '0'))
          .join('');
        return hashHex})
    document.getElementById("id_hash").value = hash
    form.submit()
})