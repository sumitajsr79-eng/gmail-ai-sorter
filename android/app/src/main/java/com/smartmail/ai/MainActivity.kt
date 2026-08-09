package com.smartmail.ai

import android.annotation.SuppressLint
import android.content.Context
import android.os.Build
import android.os.Bundle
import android.webkit.*
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val PREFS_NAME = "SmartMailPrefs"
    private val KEY_SERVER_URL = "server_url"
    private val LOCAL_ASSET_URL = "file:///android_asset/www/index.html"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        webView = WebView(this)
        setContentView(webView)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            allowFileAccess = true
            allowContentAccess = true
            useWideViewPort = true
            loadWithOverviewMode = true
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                return false
            }

            @RequiresApi(Build.VERSION_CODES.M)
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                if (request?.isForMainFrame == true) {
                    webView.loadUrl(LOCAL_ASSET_URL)
                }
            }

            @Suppress("DEPRECATION")
            override fun onReceivedError(
                view: WebView?,
                errorCode: Int,
                description: String?,
                failingUrl: String?
            ) {
                webView.loadUrl(LOCAL_ASSET_URL)
            }
        }

        loadApp()
    }

    private fun loadApp() {
        val prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val savedUrl = prefs.getString(KEY_SERVER_URL, LOCAL_ASSET_URL) ?: LOCAL_ASSET_URL
        webView.loadUrl(savedUrl)
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
