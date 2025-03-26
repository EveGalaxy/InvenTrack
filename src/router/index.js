import { createRouter, createWebHistory } from 'vue-router'
import BeaconForm from './components/BeaconForm.vue'
import DataTable from './components/DataTable.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: BeaconForm},
        { path: '/ShowData', name: 'ShowData', component: DataTable}
    ]
})

export default router