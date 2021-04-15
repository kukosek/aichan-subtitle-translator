import {faRedo, faDownload, faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons'
require('dotenv').config()
export default {
	// Target (https://go.nuxtjs.dev/config-target)
	target: 'static',
	serverMiddleware: [
	],
	router: {
		base: '/aichan/'
	},
	// Global page headers (https://go.nuxtjs.dev/config-head)
	head: {
		title: 'sub translator - ai-chan',
		meta: [
			{charset: 'utf-8'},
			{name: 'msapplication-TileColor', content: '#da532c'},
			{name: 'theme-color', content: '#ffffff'},
			{name: 'viewport', content: 'width=device-width, initial-scale=1'},
			{hid: 'description', name: 'description', content: ''}
		],
		link: [
			{rel: 'icon', type: 'image/x-icon', href: 'favicon.ico'},
			{rel: "apple-touch-icon", sizes: "180x180", href: "apple-touch-icon.png"},
			{rel: "icon", type: "image/png", sizes: "32x32", href: "favicon-32x32.png"},
			{rel: "icon", type: "image/png", sizes: "16x16", href: "favicon-16x16.png"},
			{rel: "manifest", href: "site.webmanifest"},
			{rel: "mask-icon", href: "safari-pinned-tab.svg", color: "#5bbad5"}
		]
	},

	// Global CSS (https://go.nuxtjs.dev/config-css)
	css: [
	],

	// Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
	plugins: [
	],

	// Auto import components (https://go.nuxtjs.dev/config-components)
	components: true,

	// Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
	buildModules: [
		// https://go.nuxtjs.dev/typescript
		'@nuxt/typescript-build',
	],

	// Modules (https://go.nuxtjs.dev/config-modules)
	modules: [
		// https://go.nuxtjs.dev/chakra
		'@chakra-ui/nuxt',
		// https://go.nuxtjs.dev/emotion
		'@nuxtjs/emotion',
	],

	// Build Configuration (https://go.nuxtjs.dev/config-build)
	build: {
	},
	chakra: {
		icons: {
			// Here we state that we use `fa`
			// icons library for Chakra's
			// internal icon parser
			iconPack: 'fa',
			iconSet: {
				faRedo,
				faExternalLinkAlt,
				faDownload
			}
		},
		config: {
			/**
			 * Setting this value to false disables
			 * component auto-import in your Vue templates
			 * @type {Boolean}
			 **/
			autoImport: true
		}
	},
	publicRuntimeConfig: {
		apiHttpEndpoint: process.env.API_ENDPOINT.toString(),
	},

}
