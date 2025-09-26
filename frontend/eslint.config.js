/*
 * @Author: qiuzx
 * @Date: 2025-09-12 10:05:21
 * @LastEditors: qiuzx
 * @Description: ESLint配置 - TypeScript版本
 */
import js from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsparser from "@typescript-eslint/parser";
import vue from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";

export default [
  js.configs.recommended,
  ...vue.configs["flat/recommended"],
  {
    ignores: [
      "dist/**",
      "node_modules/**",
      "*.min.js",
      "*.bundle.js"
    ]
  },
  {
    files: ["**/*.{js,ts,vue}"],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: "module",
        ecmaFeatures: {
          jsx: true
        }
      },
      globals: {
        console: "readonly",
        process: "readonly",
        Buffer: "readonly",
        __dirname: "readonly",
        __filename: "readonly",
        global: "readonly",
        module: "readonly",
        require: "readonly",
        exports: "readonly",
        localStorage: "readonly",
        window: "readonly",
        WebSocket: "readonly",
        NodeJS: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        document: "readonly",
        navigator: "readonly",
        history: "readonly",
        location: "readonly",
        Event: "readonly",
        MessageEvent: "readonly",
        CloseEvent: "readonly",
        FormData: "readonly",
        Blob: "readonly",
        File: "readonly",
        Element: "readonly",
        Node: "readonly",
        MouseEvent: "readonly"
      }
    },
    plugins: {
      "@typescript-eslint": tseslint
    },
    rules: {
      // TypeScript 规则
      "@typescript-eslint/no-unused-vars": "warn",
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/explicit-function-return-type": "off",
      "@typescript-eslint/explicit-module-boundary-types": "off",
      "@typescript-eslint/no-inferrable-types": "off",
      "@typescript-eslint/no-var-requires": "off",

      // 强制使用双引号
      quotes: ["error", "double", { allowTemplateLiterals: true }],
      "jsx-quotes": ["error", "prefer-double"],

      // Vue 相关规则
      "vue/multi-word-component-names": "off",
      "vue/no-unused-vars": "error",
      "vue/no-multiple-template-root": "off",

      // 通用规则
      "no-unused-vars": "off", // 使用TypeScript版本
      "no-console": "warn",
      "no-debugger": "error",
      "prefer-const": "error",
      "no-var": "error",

      // 代码风格
      indent: ["error", 2],
      semi: ["error", "always"],
      "comma-dangle": ["error", "never"],
      "object-curly-spacing": ["error", "always"],
      "array-bracket-spacing": ["error", "never"],
      "space-before-function-paren": ["error", "never"],
      "keyword-spacing": ["error", { before: true, after: true }],
      "space-infix-ops": "error",
      "eol-last": ["error", "always"],
      "no-trailing-spaces": "error"
    }
  },
  {
    files: ["**/*.vue"],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsparser,
        ecmaVersion: 2022,
        sourceType: "module"
      }
    },
    rules: {
      // Vue 文件特殊规则
      "vue/html-quotes": ["error", "double"],
      "vue/component-definition-name-casing": ["error", "PascalCase"],
      "vue/component-name-in-template-casing": ["error", "PascalCase"],
      "vue/attribute-hyphenation": ["error", "always"],
      "vue/v-on-event-hyphenation": ["error", "always"],
      "vue/max-attributes-per-line": "off",
      "vue/first-attribute-linebreak": "off",
      "vue/html-indent": "off",
      "vue/html-closing-bracket-newline": "off"
    }
  }
];
