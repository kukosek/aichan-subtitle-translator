<template>
	<c-flex
		margin="5px"
		:p="3"
		rounded="lg"
		border-width="1px"
		align="center"
		justify="space-between"
		v-bind="mainStyles[colorMode]"
	>
		<c-text fontSize="sm"  is-truncated>{{ fileName }} <br></c-text>
		<c-flex height="40px" width="40px" justify="center" align="center">
			<transition name="fade" mode="out-in">
				<c-spinner key=1 v-if="translateLoading" :color="mainStyles[colorMode].spinner" />
				<c-icon-button key=2 v-if="translateError" variant-color="red" aria-label="retry" icon="redo" @click="send()" />
				<c-icon-button key=3 v-if="translateSuccess" variant-color="blue" aria-label="Download" icon="download" @click="download()" />
			</transition>
		</c-flex>
	</c-flex>
</template>

<style scoped>

.fade-enter-active,
.fade-leave-active {
    transition: opacity .5s
}

.fade-enter,
.fade-leave-to {
    opacity: 0
}
</style>

<script lang="ts">

import { Component, Watch, Vue, Inject, Prop } from 'vue-property-decorator'
import { saveAs } from 'file-saver'

interface TranslateReqBody {
	src_lang: string,
	tgt_lang: string,
	format: string,
	src: string
}
interface TranslateResBody {
	readonly status: "success" | "fail" | "error",
	readonly data?: TranslateReqBody
}

@Component(
	{
		name: "FileTranslateView"
	}
)
export default class FileTranslateView extends Vue {
	@Prop(String) readonly fileName: string | undefined;
	@Prop(String) fileContents!: string;
	@Prop(String) fileFormat!: string;
	@Prop(String) srcLangCode!: string;
	@Prop(String) tgtLangCode!: string;
	private translatedContents: string = "";

	private translateSuccess : Boolean = false
	private translateError : Boolean = false
	private translateLoading : Boolean = false

	private xmlhttp : XMLHttpRequest = new XMLHttpRequest()


	private mainStyles: Object = {
		dark: {
		  bg: '#3d4756',
		  borderColor: 'whiteAlpha.200',
		  color: 'grey.200',
		  spinner: 'blue.200'
		},
		light: {
		  bg: 'white',
		  borderColor: 'grey.300',
		  color: 'grey.400',
		  spinner: 'blue.500'
		}

	  }
	@Inject('toast') private toast!: (props: Object) => void
	@Inject('$chakraColorMode') private chakraColorMode!: () => string
	@Inject('$toggleColorMode') private toggleColorMode!: () => void
	get colorMode(): string {
	  return this.chakraColorMode()
	}

	@Watch('srcLangCode')
	onPropertyChanged(value: string, oldValue: string) {
		this.send()
	}


	@Watch('tgtLangCode')
	onTgtLangChanged(value: string, oldValue: string) {
		this.send()
	}

	public download() : void {
		var blob = new Blob([this.translatedContents], {type: "application/x-ssa;charset=utf-8"});
		const fileNameSplitted : String[] = this.fileName!.split('.')
		fileNameSplitted[fileNameSplitted.length-2] += '_' + this.tgtLangCode.toUpperCase()

		saveAs(blob, fileNameSplitted.join('.'));
	}

	public send() : void {
		this.xmlhttp.abort()
		this.translateLoading = true
		this.translateError = false
		this.translatedContents = ""
		this.translateSuccess = false

		var theUrl = this.$config.apiHttpEndpoint;

		this.xmlhttp.open("POST", theUrl);
		this.xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		const reqBody : TranslateReqBody = {
			src_lang: this.srcLangCode,
			tgt_lang: this.tgtLangCode,
			format: this.fileFormat,
			src: this.fileContents
		}
		this.xmlhttp.send(JSON.stringify(reqBody))
	}

	created() {
		const view = this
		this.xmlhttp.onload = function(e: ProgressEvent) {
			view.translateLoading = false
			var jsonResponse : TranslateResBody
			try {
				jsonResponse = JSON.parse(view.xmlhttp.responseText)
				if (jsonResponse.status == "success") {
					view.translatedContents = jsonResponse.data!.src
					view.$emit("result", {
						fileName: view.fileName,
						result: view.translatedContents
					});
					view.translateSuccess = true
				}else if (jsonResponse.status == "fail") {
					view.translateError = true
					view.toast({
						title: 'Failed translating '+view.fileName+'.',
						description: "You provided bad data",
						status: 'error',
						duration: 5000,
						isClosable: true
					})
				}else if (jsonResponse.status == "error") {
					view.translateError = true
					view.toast({
						title: 'Failed translating '+view.fileName+'.',
						description: "Server error happened :(",
						status: 'error',
						duration: 5000,
						isClosable: true
					})
				}
			} catch(e) {

				view.translateError = true
				view.toast({
					title: 'Failed translating '+view.fileName+'.',
					description: "Couldn't parse json response.",
					status: 'error',
					duration: 5000,
					isClosable: true
				})
			}
		}
		this.xmlhttp.onerror = function(e: ProgressEvent) {
			view.translateLoading = false
			view.translateError = true
			view.toast({
				title: 'Failed translating '+view.fileName+'.',
				description: "Couldn't send request.",
				status: 'error',
				duration: 5000,
				isClosable: true
			})

		}
	}

	mounted() {
		this.send()
	}
}
</script>
