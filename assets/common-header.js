/* ==========================================================================
   ImpactMojo — Common Header (single source of truth)
   Injects the shared navigation into <div id="im-common-header"></div>,
   wires dropdowns + mobile menu + theme toggle, and highlights the active
   page. No dependencies. Theme state uses the same 'im-theme' localStorage
   key + data-theme attribute the pages already rely on.
   ========================================================================== */
(function () {
    'use strict';

    var LOGO = 'https://www.impactmojo.in/assets/images/ImpactMojo%20Logo.png';

    // Local (this-site) pages + the parent-ecosystem back-links.
    // Root-absolute hrefs so the header works from any directory (e.g. /m/<id>.html).
    var LOCAL_LINKS = [
        { key: 'nav.atlas', label: 'Atlas', href: '/index.html', match: ['', 'index.html'] },
        { key: 'nav.interactive', label: 'Interactive', href: '/explore.html', match: ['explore.html'] },
        { key: 'nav.stories', label: 'Stories', href: '/stories.html', match: ['stories.html'] },
        { key: 'nav.methodology', label: 'Methodology', href: '/methodology.html', match: ['methodology.html'] }
    ];

    var PARENT_LINKS = [
        { key: 'nav.home', label: 'Home', href: 'https://www.impactmojo.in/' },
        { key: 'nav.catalogue', label: 'Catalogue', href: 'https://www.impactmojo.in/catalog' },
        { key: 'nav.courses', label: 'Courses', href: 'https://www.impactmojo.in/courses/' },
        { key: 'nav.specials', label: 'Specials', href: 'https://www.impactmojo.in/#specials' },
        { key: 'nav.about', label: 'About', href: 'https://www.impactmojo.in/about' }
    ];

    /* ── i18n framework (matches the parent site's data-i18n pattern) ── */
    var I18N = {
        'nav.atlas': { en: 'Atlas', hi: 'एटलस' },
        'nav.interactive': { en: 'Interactive', hi: 'इंटरैक्टिव' },
        'nav.stories': { en: 'Stories', hi: 'कहानियाँ' },
        'nav.methodology': { en: 'Methodology', hi: 'पद्धति' },
        'nav.impactmojo': { en: 'ImpactMojo', hi: 'इम्पैक्टमोजो' },
        'nav.explore': { en: 'Explore the platform', hi: 'मंच देखें' },
        'nav.home': { en: 'Home', hi: 'होम' },
        'nav.catalogue': { en: 'Catalogue', hi: 'सूची' },
        'nav.courses': { en: 'Courses', hi: 'पाठ्यक्रम' },
        'nav.specials': { en: 'Specials', hi: 'विशेष' },
        'nav.about': { en: 'About', hi: 'परिचय' },
        'logo.tagline': { en: 'An ImpactMojo Atlas', hi: 'एक इम्पैक्टमोजो एटलस' },
        'lang.toggle': { en: 'हिन्दी', hi: 'EN' }
    };
    var IM = window.IM = window.IM || {};
    IM.lang = localStorage.getItem('im-lang') || 'en';
    function dict() { return Object.assign({}, I18N, window.IM_I18N || {}); }
    IM.t = function (key) { var e = dict()[key] || {}; return e[IM.lang] || e.en || key; };
    IM.applyI18n = function (root) {
        var scope = root || document;
        scope.querySelectorAll('[data-i18n]').forEach(function (el) {
            var v = IM.t(el.getAttribute('data-i18n'));
            if (v) el.textContent = v;
        });
        document.documentElement.lang = IM.lang;
    };
    IM.setLang = function (l) {
        IM.lang = l;
        localStorage.setItem('im-lang', l);
        IM.applyI18n();
        window.dispatchEvent(new CustomEvent('im:langchange', { detail: l }));
    };

    var THEMES = [
        { key: 'system', title: 'System theme', path: '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>' },
        { key: 'light', title: 'Light theme', path: '<circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>' },
        { key: 'dark', title: 'Dark theme', path: '<path d="M21 12.79A9 9 0 1111.21 3a7 7 0 009.79 9.79z"/>' }
    ];

    function currentPage() {
        var p = location.pathname.split('/').pop() || '';
        return p.toLowerCase();
    }

    function isActive(link) {
        var page = currentPage();
        return link.match && link.match.indexOf(page) !== -1;
    }

    function svg(inner) {
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
            'stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>';
    }

    function build() {
        var localItems = LOCAL_LINKS.map(function (l) {
            return '<li><a href="' + l.href + '" data-i18n="' + l.key + '"' + (isActive(l) ? ' class="im-active" aria-current="page"' : '') +
                '>' + IM.t(l.key) + '</a></li>';
        }).join('');

        var parentItems = PARENT_LINKS.map(function (l) {
            return '<li><a class="im-ext" href="' + l.href + '" data-i18n="' + l.key + '">' + IM.t(l.key) + '</a></li>';
        }).join('');

        var themeBtns = THEMES.map(function (t) {
            return '<button class="im-theme-btn" data-theme="' + t.key + '" title="' + t.title +
                '" aria-label="' + t.title + '">' + svg(t.path) + '</button>';
        }).join('');

        return '' +
        '<nav class="im-nav" aria-label="Primary">' +
            '<a class="im-logo" href="https://www.impactmojo.in" aria-label="ImpactMojo home">' +
                '<img src="' + LOGO + '" alt="ImpactMojo" width="40" height="40" fetchpriority="high">' +
                '<span class="im-logo-text">' +
                    '<span class="im-logo-main">How India Lives</span>' +
                    '<span class="im-logo-tagline" data-i18n="logo.tagline">' + IM.t('logo.tagline') + '</span>' +
                '</span>' +
            '</a>' +
            '<ul class="im-links" id="im-links">' +
                localItems +
                '<li class="im-has-dropdown">' +
                    '<button class="im-dropdown-toggle" type="button" aria-expanded="false" aria-haspopup="true">' +
                        '<span data-i18n="nav.impactmojo">' + IM.t('nav.impactmojo') + '</span>' + svg('<path d="M6 9l6 6 6-6"/>').replace('<svg', '<svg class="im-dropdown-arrow"') +
                    '</button>' +
                    '<ul class="im-dropdown">' +
                        '<li class="im-dropdown-label" data-i18n="nav.explore">' + IM.t('nav.explore') + '</li>' +
                        parentItems +
                    '</ul>' +
                '</li>' +
                // Theme + language live inside the menu on mobile (keeps the top bar to logo + burger)
                '<li class="im-menu-extra">' +
                    '<div class="im-theme" role="group" aria-label="Theme">' + themeBtns + '</div>' +
                    '<button class="im-lang" type="button" aria-label="Switch language" data-i18n="lang.toggle">' + IM.t('lang.toggle') + '</button>' +
                '</li>' +
            '</ul>' +
            '<div class="im-actions">' +
                '<button class="im-lang" type="button" aria-label="Switch language" data-i18n="lang.toggle">' + IM.t('lang.toggle') + '</button>' +
                '<div class="im-theme" role="group" aria-label="Theme">' + themeBtns + '</div>' +
                '<button class="im-burger" id="im-burger" type="button" aria-label="Toggle menu" aria-expanded="false">' +
                    '<span></span><span></span><span></span>' +
                '</button>' +
            '</div>' +
        '</nav>';
    }

    /* ── Theme ── */
    function applyTheme(mode) {
        if (mode === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('im-theme', 'dark');
        } else if (mode === 'light') {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('im-theme', 'light');
        } else {
            localStorage.removeItem('im-theme');
            if (window.matchMedia('(prefers-color-scheme:dark)').matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
            } else {
                document.documentElement.removeAttribute('data-theme');
            }
        }
    }

    function markActiveTheme(header) {
        var mode = localStorage.getItem('im-theme') || 'system';
        header.querySelectorAll('.im-theme-btn').forEach(function (b) {
            b.classList.toggle('im-active', b.dataset.theme === mode);
        });
    }

    function wire(header) {
        // Theme buttons
        header.querySelectorAll('.im-theme-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                applyTheme(btn.dataset.theme);
                markActiveTheme(header);
            });
        });
        markActiveTheme(header);

        // Dropdowns
        header.querySelectorAll('.im-has-dropdown').forEach(function (dd) {
            var toggle = dd.querySelector('.im-dropdown-toggle');
            toggle.addEventListener('click', function (e) {
                e.stopPropagation();
                var open = dd.classList.toggle('im-open');
                toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            });
            // Hover open on desktop
            dd.addEventListener('mouseenter', function () {
                if (window.innerWidth > 860) dd.classList.add('im-open');
            });
            dd.addEventListener('mouseleave', function () {
                if (window.innerWidth > 860) {
                    dd.classList.remove('im-open');
                    toggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
        document.addEventListener('click', function () {
            header.querySelectorAll('.im-has-dropdown.im-open').forEach(function (dd) {
                dd.classList.remove('im-open');
                var t = dd.querySelector('.im-dropdown-toggle');
                if (t) t.setAttribute('aria-expanded', 'false');
            });
        });

        // Mobile menu
        var burger = header.querySelector('#im-burger');
        burger.addEventListener('click', function (e) {
            e.stopPropagation();
            var open = header.classList.toggle('im-menu-open');
            burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        });

        // Language toggle (one in the top bar for desktop, one in the menu for mobile)
        header.querySelectorAll('.im-lang').forEach(function (lang) {
            lang.addEventListener('click', function () {
                IM.setLang(IM.lang === 'en' ? 'hi' : 'en');
            });
        });
    }

    function init() {
        var mount = document.getElementById('im-common-header');
        if (!mount) return;
        mount.innerHTML = build();
        mount.classList.add('im-header');
        // Ensure the header element itself carries the styling class + role.
        mount.setAttribute('role', 'banner');
        wire(mount);
        // Translate the header + any page [data-i18n] elements to the saved language.
        IM.applyI18n();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
