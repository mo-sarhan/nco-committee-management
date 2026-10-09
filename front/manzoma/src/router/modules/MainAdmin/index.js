import { icons } from '../../../../public/icons'
import MainAdminLayout from '@/layouts/MainAdminLayout.vue'
import defaultLayout from '@/layouts/default.vue'
import Index from '@/views/mainAdmin/Index.vue'
import lagnaData from '@/views/mainAdmin/lagna/Index.vue'
import lagnaMembers from '@/views/mainAdmin/lagna/Index.vue'
import lagnaJudg from '@/views/mainAdmin/lagna/Index.vue'
import Users from '@/views/mainAdmin/Users.vue'
import AfrPersons from '@/views/mainAdmin/afrPersons/Index.vue'
import Profile from '@/views/mainAdmin/afrPersons/profile.vue'
import profileImageUpload from '@/views/mainAdmin/afrPersons/profileImageUpload.vue'
import AfrPersonsReports from '@/views/mainAdmin/afrPersons/AfrpersonReports/index.vue'
import uploadedImagesReport from '@/views/mainAdmin/afrPersons/AfrpersonReports/uploadedImagesReport/index.vue'
import unitsImagesReport from '@/views/mainAdmin/afrPersons/AfrpersonReports/uploadedImagesReport/unitsImagesReport.vue'
import personsImagesReport from '@/views/mainAdmin/afrPersons/AfrpersonReports/uploadedImagesReport/personsImagesReport.vue'
import lagnaDetails from '@/views/mainAdmin/lagna/lagnaDetails.vue'
import lagaSpecificData from '@/views/mainAdmin/lagna/lagaSpecificData.vue'
import specificLagnaPersonProfile from '@/views/mainAdmin/lagna/specificLagnaPersonProfile.vue'
import Reports from '@/views/mainAdmin/reports/index.vue'
import commitiReportData from '@/views/mainAdmin/reports/commitiReportData/index.vue'
import Settings from '@/views/mainAdmin/Settings.vue'

import presenting from '@/views/presentation/presenting/presenting.vue'
import LagnasPresenting from '@/views/presentation/presenting/index.vue'
import AdminPanelWindow from '@/views/presentation/AdminControle/AdminPanelWindow.vue'
import AdminControle from '@/views/presentation/AdminControle/index.vue'
export default [
  {
    path: '/main-admin',
    component: MainAdminLayout,
    meta: {
      label: 'الرئيسية',
      menu: true,
      icon: icons.Dashboard,
      requiresAuth: true,
    },
    children: [
      {
        path: '',
        redirect: '/main-admin/afr-persons',
      },
      {
        path: '/main-admin/afr-persons',
        meta: {
          label: 'بيانات الراتب العالى',
          menu: true,
          sidebar: true,
          icon: icons.User,
          requiresAuth: true,
        },
        children: [
          {
            path: '/main-admin/afr-persons',
            name: 'AfrPersons',
            component: AfrPersons,
            meta: {
              label: 'البيانات الاساسية للراتب العالى',
              menu: true,
              sidebar: true,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/afr-persons/profile/:id?/:person_name?/:committe_code?/:spacific_id?/:person_id?',
            name: 'AfrPersonProfile',
            component: Profile,
            meta: {
              label: (route) => ' عرض - ' + route.params.person_name || 'الملف الشخصي',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/afr-persons/profile-image-upload/:id/:person_name',
            name: 'profileImageUpload',
            component: profileImageUpload,
            meta: {
              label: (route) => 'رفع صور - ' + route.params.person_name || 'رفع صور الراتب العالى',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/afr-persons/reports',
            name: 'AfrPersonsReports',
            component: AfrPersonsReports,
            meta: {
              label: 'التقارير',
              menu: true,
              sidebar: true,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/afr-persons/reports/uploaded-images-report',
            name: 'uploadedImagesReport',
            component: uploadedImagesReport,
            meta: {
              label: 'تقرير رفع الصور',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/afr-persons/reports/uploaded-images-report/units-images-report/:prnt_army_code',
            name: 'unitsImagesReport',
            component: unitsImagesReport,
            meta: {
              label: 'تفاصيل وحدات التبعية',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/afr-persons/reports/uploaded-images-report/persons-images-report/:prnt_army_code/:unit_code?/',
            name: 'personsImagesReport',
            component: personsImagesReport,
            meta: {
              label: 'تفاصيل افراد التبعية',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
        ],
      },
      {
        path: '/main-admin/lagna',
        meta: {
          label: 'اللجان',
          menu: true,
          sidebar: true,
          icon: icons.Briefcase,
          requiresAuth: true,
        },
        children: [
          {
            path: '/main-admin/lagna',
            name: 'lagnaData',
            component: lagnaData,
            meta: {
              label: 'بيانات اللجان',
              menu: true,
              sidebar: true,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/lagna/lagna-specific-data/:committe_code/:committe_name',
            name: 'lagaSpecificData',
            component: lagaSpecificData,
            meta: {
              label: (route) => ' عرض - ' + route.params.committe_name || 'الملف الشخصي',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/lagna/lagna-specific-data/lagna-details/specific-lagna-person-profile/:id?/:person_name?/:committe_code?/:spacific_id?/:person_id?',
            name: 'specificLagnaPersonProfile',
            component: specificLagnaPersonProfile,
            meta: {
              label: (route) => ' عرض - ' + route.params.person_name || 'الملف الشخصي',
              breadcrumbParent: 'lagnaDetails',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/lagna/lagna-specific-data/lagna-details/:committe_code?/:spacific_id?/:specific_name?/:committe_name',
            name: 'lagnaDetails',
            component: lagnaDetails,
            meta: {
              label: (route) => ' عرض - ' + route.params.specific_name || 'تفاصيل اللجنة',
              breadcrumbParent: 'lagaSpecificData',
              menu: false,
              sidebar: false,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/lagna/lagn-members',
            name: 'lagnaMembers',
            component: lagnaMembers,
            meta: {
              label: 'افراد اللجان',
              menu: true,
              sidebar: true,
              requiresAuth: true,
            },
          },
          {
            path: '/main-admin/lagna/lagna-judg',
            name: 'lagnaJudg',
            component: lagnaJudg,
            meta: {
              label: 'اعضاء اللجان',
              menu: true,
              sidebar: true,
              requiresAuth: true,
            },
          },
        ],
      },
      {
        path: '/presentation',
        // component: defaultLayout,
        meta: {
          label: 'شاشة تنفيذ اللجان',
          menu: true,
          icon: icons.Briefcase,
          sidebar: true,
          requiresAuth: true,
        },
        children: [
          {
            path: '/presentation/lagnas-presenting',
            name: 'LagnasPresenting',
            component: LagnasPresenting,
            meta: {
              label: 'شاشة العرض',
              menu: true,
              sidebar: true,
              // requiresAuth:true
            },
          },
          {
            path: '/presentation/lagnas-presenting/presenting/:committe_code?/:committe_name?',
            name: 'presenting',
            component: presenting,
            meta: {
              label: 'شاشة العرض',
              menu: true,
              sidebar: false,
              // requiresAuth:true
            },
          },
          {
            path: '/presentation/admin-controle/admin-panel-window/:committe_code?/:committe_name?',
            name: 'AdminPanelWindow',
            component: AdminPanelWindow,
            meta: {
              label: 'شاشة التحكم فى عرض اللجنة',
              menu: true,
              sidebar: false,
              // requiresAuth:true
            },
          },
          {
            path: '/presentation/admin-controle',
            name: 'AdminControle',
            component: AdminControle,
            meta: {
              label: 'شاشة التحكم فى عرض اللجنة',
              menu: true,
              sidebar: true,
              // requiresAuth:true
            },
          },
        ],
      },
      // {
      //   path: 'users',
      //   name: 'Users',
      //   component: Users,
      //   meta: {
      //     label: 'المستخدمين',
      //     menu: true,
      //     sidebar: true,
      //     icon: icons.User,
      //   },
      // },
      {
        path: 'reports',
        name: 'Reports',
        component: Reports,
        meta: {
          label: 'التقارير',
          menu: true,
          sidebar: true,
          icon: icons.FileText,
        },
      },
      {
        path: '/main-admin/reports/commiti-report-data',
        name: 'commitiReportData',
        component: commitiReportData,
        meta: {
          label: 'تقرير بيانات اللجان',
          menu: false,
          sidebar: false,
          requiresAuth: true,
        },
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: {
          label: 'إعدادات شكل الصفحات',
          menu: true,
          sidebar: true,
          icon: icons.Settings,
          requiresAuth: true,
        },
      },
    ],
  },
]
