<template>
    <div>

    </div>
</template>

<script>


export default {

    name: 'Logout',
    mounted: function () {
        let qs = require('qs');
        let headers= {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + btoa(this.$getClient_id()+ ':' + this.$getClient_secret())
            }
        let tok = {
            'token': this.$session.get('access'),
            'token_type_hint': 'access_token',
        }
        this.$axios.post('/oauth2/revoke', qs.stringify(tok) , {headers: headers})
            .catch()
        this.$session.destroy();
        window.location.reload(true);
    },
}
</script>
