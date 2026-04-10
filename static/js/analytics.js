(function () {
    function normalizeText(value) {
        return String(value || '')
            .replace(/\s+/g, ' ')
            .trim()
            .slice(0, 120);
    }

    function getPagePath() {
        return window.location.pathname + window.location.search;
    }

    function getPageType(pathname) {
        if (pathname === '/') {
            return 'landing';
        }
        if (pathname.indexOf('/dashboard/') === 0) {
            return 'dashboard';
        }
        if (pathname.indexOf('/school/') === 0) {
            return 'school';
        }
        if (pathname.indexOf('/login/') === 0 || pathname.indexOf('/register/') === 0) {
            return 'auth';
        }
        if (pathname.indexOf('/admin/') === 0) {
            return 'admin';
        }
        return 'public';
    }

    function track(eventName, params) {
        if (typeof window.gtag !== 'function') {
            return;
        }
        window.gtag('event', eventName, params || {});
    }

    function getElementLabel(element) {
        if (!element) {
            return 'unknown';
        }

        var explicitLabel = element.getAttribute('data-ga-label') ||
            element.getAttribute('aria-label') ||
            element.getAttribute('title');

        if (explicitLabel) {
            return normalizeText(explicitLabel);
        }

        var text = normalizeText(
            element.innerText ||
            element.value ||
            element.textContent ||
            element.id ||
            element.name
        );

        if (text) {
            return text;
        }

        return normalizeText(element.tagName || 'element').toLowerCase();
    }

    function getSectionName(element) {
        var current = element;

        while (current && current !== document.body) {
            if (current.dataset && current.dataset.gaSection) {
                return normalizeText(current.dataset.gaSection);
            }
            if (current.id) {
                return normalizeText(current.id);
            }
            current = current.parentElement;
        }

        return 'page';
    }

    function getFormName(form) {
        if (!form) {
            return 'form';
        }

        var actionUrl = toUrl(form.getAttribute('action') || window.location.href);
        var actionPath = actionUrl ? (actionUrl.pathname + actionUrl.search) : getPagePath();

        return normalizeText(
            form.getAttribute('data-ga-form') ||
            form.getAttribute('aria-label') ||
            form.id ||
            form.getAttribute('name') ||
            actionPath ||
            'form'
        );
    }

    function toUrl(href) {
        if (!href) {
            return null;
        }

        try {
            return new URL(href, window.location.origin);
        } catch (error) {
            return null;
        }
    }

    function isDownloadLink(element, url) {
        if (!element || !url) {
            return false;
        }

        if (element.hasAttribute('download')) {
            return true;
        }

        return /\.(pdf|doc|docx|xls|xlsx|csv|zip|ppt|pptx)$/i.test(url.pathname);
    }

    function getContactMethod(url) {
        if (!url) {
            return '';
        }

        if (url.protocol === 'mailto:') {
            return 'email';
        }
        if (url.protocol === 'tel:') {
            return 'phone';
        }
        if (url.hostname === 'wa.me' || url.hostname === 'api.whatsapp.com') {
            return 'whatsapp';
        }

        return '';
    }

    function trackPageView() {
        track('page_view', {
            page_title: document.title,
            page_location: window.location.href,
            page_path: getPagePath(),
            page_referrer: document.referrer || '',
            page_type: getPageType(window.location.pathname)
        });
    }

    function trackScrollDepth() {
        var thresholds = [25, 50, 75, 90];
        var trackedDepths = {};
        var ticking = false;

        function updateDepth() {
            var doc = document.documentElement;
            var scrollableHeight = doc.scrollHeight - window.innerHeight;

            if (scrollableHeight <= 0) {
                return;
            }

            var percentScrolled = Math.round((window.scrollY / scrollableHeight) * 100);

            thresholds.forEach(function (threshold) {
                if (percentScrolled >= threshold && !trackedDepths[threshold]) {
                    trackedDepths[threshold] = true;
                    track('scroll_depth', {
                        percent_scrolled: threshold,
                        page_path: getPagePath(),
                        page_type: getPageType(window.location.pathname)
                    });
                }
            });
        }

        function onScroll() {
            if (ticking) {
                return;
            }

            ticking = true;
            window.requestAnimationFrame(function () {
                updateDepth();
                ticking = false;
            });
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        updateDepth();
    }

    function trackSectionViews() {
        if (!('IntersectionObserver' in window)) {
            return;
        }

        var sectionIds = {};

        Array.prototype.forEach.call(document.querySelectorAll('a[href^="#"]'), function (link) {
            var href = link.getAttribute('href');
            if (href && href.length > 1) {
                sectionIds[href.slice(1)] = true;
            }
        });

        var trackedSections = {};
        var sections = Object.keys(sectionIds)
            .map(function (id) { return document.getElementById(id); })
            .filter(Boolean);

        if (!sections.length) {
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting || entry.intersectionRatio < 0.5) {
                    return;
                }

                var sectionId = entry.target.id;
                if (trackedSections[sectionId]) {
                    return;
                }

                trackedSections[sectionId] = true;
                track('section_view', {
                    section_name: normalizeText(sectionId),
                    page_path: getPagePath(),
                    page_type: getPageType(window.location.pathname)
                });
            });
        }, {
            threshold: 0.5
        });

        sections.forEach(function (section) {
            observer.observe(section);
        });
    }

    function trackFormSubmissions() {
        document.addEventListener('submit', function (event) {
            var form = event.target;
            if (!form || form.tagName !== 'FORM') {
                return;
            }

            var actionUrl = toUrl(form.getAttribute('action') || window.location.href);
            var actionPath = actionUrl ? (actionUrl.pathname + actionUrl.search) : getPagePath();

            track('form_submit', {
                form_name: getFormName(form),
                form_id: normalizeText(form.id || form.getAttribute('name') || actionPath || 'form'),
                form_method: normalizeText(form.getAttribute('method') || 'get').toLowerCase(),
                form_action: actionPath,
                section_name: getSectionName(form),
                page_path: getPagePath(),
                page_type: getPageType(window.location.pathname)
            });
        });
    }

    function trackClicks() {
        document.addEventListener('click', function (event) {
            var target = event.target;
            if (!target) {
                return;
            }

            if (target.nodeType !== 1) {
                target = target.parentElement;
            }

            if (!target || typeof target.closest !== 'function') {
                return;
            }

            var element = target.closest('a, button, input[type="button"], input[type="submit"]');
            if (!element) {
                return;
            }

            var baseParams = {
                click_label: getElementLabel(element),
                section_name: getSectionName(element),
                page_path: getPagePath(),
                page_type: getPageType(window.location.pathname)
            };

            if (element.tagName === 'A') {
                var href = element.getAttribute('href');
                if (!href || href === '#' || href.indexOf('javascript:') === 0) {
                    return;
                }

                var url = toUrl(href);
                if (!url) {
                    return;
                }

                var contactMethod = getContactMethod(url);
                if (contactMethod) {
                    track('contact_click', {
                        contact_method: contactMethod,
                        destination: href,
                        click_label: baseParams.click_label,
                        section_name: baseParams.section_name,
                        page_path: baseParams.page_path,
                        page_type: baseParams.page_type
                    });
                    return;
                }

                if (isDownloadLink(element, url)) {
                    track('file_download', {
                        file_name: normalizeText(url.pathname.split('/').pop()),
                        file_extension: normalizeText(url.pathname.split('.').pop()).toLowerCase(),
                        destination: href,
                        click_label: baseParams.click_label,
                        section_name: baseParams.section_name,
                        page_path: baseParams.page_path,
                        page_type: baseParams.page_type
                    });
                    return;
                }

                if (href.charAt(0) === '#') {
                    track('section_nav_click', {
                        destination: href,
                        click_label: baseParams.click_label,
                        section_name: baseParams.section_name,
                        page_path: baseParams.page_path,
                        page_type: baseParams.page_type
                    });
                    return;
                }

                if (url.origin !== window.location.origin) {
                    track('outbound_click', {
                        destination: url.href,
                        link_domain: url.hostname,
                        click_label: baseParams.click_label,
                        section_name: baseParams.section_name,
                        page_path: baseParams.page_path,
                        page_type: baseParams.page_type
                    });
                    return;
                }

                track('navigation_click', {
                    destination: url.pathname + url.search + url.hash,
                    click_label: baseParams.click_label,
                    section_name: baseParams.section_name,
                    page_path: baseParams.page_path,
                    page_type: baseParams.page_type
                });
                return;
            }

            if ((element.tagName === 'BUTTON' && (element.type || '').toLowerCase() === 'submit') ||
                (element.tagName === 'INPUT' && (element.type || '').toLowerCase() === 'submit')) {
                return;
            }

            track('cta_click', {
                click_label: baseParams.click_label,
                section_name: baseParams.section_name,
                page_path: baseParams.page_path,
                page_type: baseParams.page_type
            });
        });
    }

    function init() {
        trackPageView();
        trackClicks();
        trackFormSubmissions();
        trackScrollDepth();
        trackSectionViews();

        window.aiLabAnalytics = {
            track: track
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
