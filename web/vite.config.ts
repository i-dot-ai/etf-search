import { defineConfig } from 'vite'
import postcssNesting from 'postcss-nesting'
import postcssCustomMedia from 'postcss-custom-media'
import svgLoader from 'vite-svg-loader'
import postcssColorModFunction from 'postcss-color-mod-function'
// eslint-disable-next-line import/no-named-as-default
import liveReload from 'vite-plugin-live-reload'
import postcssInlineSvg from 'postcss-inline-svg'

export default defineConfig({
  server: {
    port: 5173
  },
  plugins: [
    svgLoader({ defaultImport: 'raw' }),
    liveReload('../etf/templates/**/*.html', { alwaysReload: true })
  ],
  css: {
    postcss: {
      plugins: [
        postcssNesting,
        postcssCustomMedia,
        postcssColorModFunction({
          importFrom: 'src/style/vars.css'
        }),
        postcssInlineSvg({
          paths: ['public/svg']
        })
      ]
    }
  },
  build: {
    outDir: './build',
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`
      }
    }
  }
})
