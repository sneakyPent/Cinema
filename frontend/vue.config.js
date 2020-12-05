const PEP_BACKEND_HOST = 'http://data-pep-proxy-wilma:1028';
const BACKEND_HOST = 'http://application:8000';

const KEYROCK_HOST = 'http://keyrockIDM:3005';


module.exports = {
    devServer: {
        proxy: {
            ['^\\/api\\/(?!Request)(.+)\\/']: {
                target: PEP_BACKEND_HOST,
            },
            ['^\\/api\\/Request\\/'] : {
                target: BACKEND_HOST,
            },
            '/oauth2': {
                target: KEYROCK_HOST
            },
            '/admin': {
                target: PEP_BACKEND_HOST
            },
            '/v1': {
                target: KEYROCK_HOST
            },
            '/user': {
                target: KEYROCK_HOST
            },
            '^/auth': {
                target: KEYROCK_HOST
            }
        },
        host: '0.0.0.0',
        port: 80,
    },
    productionSourceMap: false,
};
