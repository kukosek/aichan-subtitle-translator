<template>
  <div class="container">
    <CBox
      v-bind="mainStyles[colorMode]"
      d="flex"
      w="100vw"
      h="100vh"
      flex-dir="column"
      justify-content="center"
    >
      <CHeading text-align="center" mb="4">
        ⚡️ Ai-Chan Sub Translator
      </CHeading>
      <CFlex justify="center" direction="column" align="center">


		  <c-stack align="center" :spacing="2" is-inline>
			  <c-text>from</c-text>
			  <c-select v-model="srcLangCode" >
				<option v-for="(name, code) in languages" :value=code :key=code>
					{{name}}
				</option>
			  </c-select>
			  <c-text>to</c-text>
			  <c-select v-model="tgtLangCode" >
				<option v-for="(name, code) in languages" :value=code :key=code>
					{{name}}
				</option>
			  </c-select>
			  <CIconButton
				mr="3"
				:icon="colorMode === 'light' ? 'moon' : 'sun'"
				:aria-label="`Switch to ${
				  colorMode === 'light' ? 'dark' : 'light'
				} mode`"
				@click="toggleColorMode"
			  />
			  <CBox>
				  <CButton
					left-icon="info"
					variant-color="blue"
					@click="open"
				  >
					About
				  </CButton>
			  </CBox>
		  </c-stack>
		 <c-modal
			  :is-open="isOpen"
			  :on-close="close"
			>
			  <c-modal-content ref="content">
				<c-modal-header>About this page</c-modal-header>
				<c-modal-close-button />
				<c-modal-body>
					<p>
						<c-link isExternal="true" href="https://github.com/kukosek/aichan-subtitle-translator">
							Github page  <c-icon name="external-link-alt" mx="2px" />
						</c-link>
					</p>
					I made this page to troll: anticeler, kdan,... and
					other anime fansubbers. Can we still be friends pls?
					<p>
					This tool is a gift for HNS translation team.
					</p>
					<p>
					If you like this, let me know, so in the future, we could theoretically
					make this just as good as
					human translators by improving the models. :)<br>
					</p>
					<p>
					This tool uses <c-link isExternal="true" href="https://lindat.mff.cuni.cz/services/translation/">
					LINDAT Translation service  <c-icon name="external-link-alt" mx="2px" /> </c-link> developed by
					<c-link isExternal="true" href="http://ufal.mff.cuni.cz/">ÚFAL  <c-icon name="external-link-alt" mx="2px" /></c-link> of MFF CUNI
					</p>
				</c-modal-body>
				<c-modal-footer>
				</c-modal-footer>
			  </c-modal-content>
			<c-modal-overlay />
    </c-modal>
		<FileTable
			:srcLangCode=srcLangCode
			:tgtLangCode=tgtLangCode
		/>

      </CFlex>
    </CBox>
  </div>
</template>

<script lang="js">
import FileTable from '../components/FileTable.vue'

export default {
  name: 'App',
  inject: ['$chakraColorMode', '$toggleColorMode'],
  data () {
    return {
		isOpen: false,
	  srcLangCode: 'en',
	  tgtLangCode: 'cs',
      languages: {
			cs: 'Czech',
			en: 'English',
			de: 'German',
			fr: 'French',
			ru: 'Russian',
			hi: 'Hindi'
		},
	  showModal: false,
      mainStyles: {
        dark: {
          bg: 'gray.700',
          color: 'whiteAlpha.900'
        },
        light: {
          bg: 'white',
          color: 'gray.900'
        }
      }
    }
  },
  provide() {
	  return {
		toast: this.$toast
	  }
  },
  computed: {
    colorMode () {
      return this.$chakraColorMode()
    },
    theme () {
      return this.$chakraTheme()
    },
    toggleColorMode () {
      return this.$toggleColorMode
    }
  },
  methods: {
	open() {
      this.isOpen = true
    },
    close() {
      this.isOpen = false
    }
  },
  watch: {
		tgtLangCode: function (new_val, old_val) {
			if (new_val == this.srcLangCode) {
				this.srcLangCode = old_val
			}
		},
		srcLangCode: function (new_val, old_val) {
			if (new_val == this.tgtLangCode) {
				this.tgtLangCode = old_val
			}
		}

	}
}
</script>
