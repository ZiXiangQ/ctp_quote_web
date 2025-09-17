/*
 * @Author: qiuzx
 * @Date: 2025-09-12 10:05:21
 * @LastEditors: qiuzx
 * @Description: description
 */
import js from "@eslint/js";
import vue from "eslint-plugin-vue";

export default [
  js.configs.recommended,
  ...vue.configs["flat/recommended"],
  {
    files: ["**/*.{js,vue}"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
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
        window: "readonly"
      }
    },
    rules: {
      // 强制使用双引号
      quotes: ["error", "double", { allowTemplateLiterals: true }],
      "jsx-quotes": ["error", "prefer-double"],

      // Vue 相关规则
      "vue/multi-word-component-names": "off",
      "vue/no-unused-vars": "error",
      "vue/no-multiple-template-root": "off",

      // 通用规则
      "no-unused-vars": "error",
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
      "space-before-function-paren": ["error", "always"],
      "keyword-spacing": ["error", { before: true, after: true }],
      "space-infix-ops": "error",
      "eol-last": ["error", "always"],
      "no-trailing-spaces": "error"
    }
  },
  {
    files: ["**/*.vue"],
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
