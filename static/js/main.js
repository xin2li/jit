// static/js/main.js
const { createApp, ref, onMounted } = Vue;


createApp({
    data() {


        const error_updatetime = ref('Loading...');
        const fx_updatetime = ref('Loading...');

        const current_errorData = ref([]);

        const formPN = ref('');
        const expandedRow = ref(null);

        

        // Function to fetch update time from API
        const fetchUpdateTime = async () => {
            try {
                const response = await axios.get('/updatetime');
                error_updatetime.value = response.data.error_updatetime;
                fx_updatetime.value = response.data.fx_updatetime;
            } catch (error) {
                console.error('Error fetching update time:', error);
                error_updatetime.value = 'Error loading time';
            }
        };

        const fetchErrorData = async () => {
            try {
                const response = await axios.get('/currenterrors');
                current_errorData.value = response.data;
 
            } catch (error) {
                console.error('Error fetching current error:', error);
                current_errorData.value = [];
            }
        };


        const handleExpand = (row) => {
            if (expandedRow.value === row) {
                // 如果点击的是已展开的行，则关闭它
                expandedRow.value = null;
            } else {
                // 展开新行并关闭之前展开的行
                expandedRow.value = row;
            }
            formPN.value = row.PN; // 将 formPN 设置为当前行的 PN
        };
     

        const optionsType = ref([
            {'type':'BOM'}, {'type':'FAKOM'}, {'type':'LAW'}, {'type':'VVT'}, {'type':'OPEN'}
        ]);

        


        // Fetch update time when component mounts
        onMounted(() => {
            fetchUpdateTime();
            fetchErrorData();
            
        });


        return {
            // activeIndex,


            // gridData,
            error_updatetime,
            fx_updatetime,

            current_errorData,
            
            optionsType,
            formPN,
            expandedRow,
            handleExpand


        };
    },

    methods: {
        // Handle menu click (if needed)
        homeClick() {
            window.location.href = '/'; // Redirect to the home page
        }
    },

    


}).use(ElementPlus).mount('#app');