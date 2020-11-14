const BACKEND_HOST = 'http://application:8000';
const KEYROCK_HOST = 'http://keyrockIDM:3005';


module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: BACKEND_HOST,
                // changeOrigin: true,
                // pathRewrite: {
                //     '^': ''
                // }
            },
            '/media': {
                target: BACKEND_HOST
            },
            '/admin/': {
                target: BACKEND_HOST
            },
            '/v1': {
                target: KEYROCK_HOST
            }
        },
        host: '0.0.0.0',
        port: 80,
    },
    productionSourceMap: false,
};
