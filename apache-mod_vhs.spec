#Module-Specific definitions
%define mod_name mod_vhs
%define mod_conf A73_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	1.0.32
Release:	21
Group:		System/Servers
License:	GPL
URL:		http://www.oav.net/projects/mod_vhs/
Source0:	http://www.oav.net/projects/mod_vhs/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	libhome-devel
BuildRequires:	php-devel

%description
mod_vhs is an Apache 2.0/2.1 Web server module allowing mass virtual hosting
without the need for file-based configuration. The virtual host paths are
translated from any database supported by libhome at request time from MySQL,
LDAP, PAM, or a system password file. PHP security can be basically
auto-configured from the database using this module.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# fix attribs
chmod 644 *

%build
%{_bindir}/apxs -DDEBIAN `apr-1-config --includes` `libhome.sh --includes` `php-config --includes` -lhome -DHAVE_MOD_PHP_SUPPORT -c %{mod_name}.c

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean

%files
%doc AUTHORS ChangeLog README* THANKS TODO WARNING
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Wed May 25 2011 Funda Wang <fwang@mandriva.org> 1.0.32-20mdv2011.0
+ Revision: 678952
- bump rel

* Wed May 25 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-19
+ Revision: 678928
- rebuild
- mass rebuild

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-17mdv2011.0
+ Revision: 627212
- rebuilt against mysql-5.5.8 libs, again
- rebuilt against mysql-5.5.8 libs

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-14mdv2011.0
+ Revision: 588085
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 1.0.32-13mdv2010.1
+ Revision: 537582
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-12mdv2010.1
+ Revision: 516246
- rebuilt for apache-2.2.15

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-11mdv2010.1
+ Revision: 507477
- rebuild

* Tue Jan 12 2010 Buchan Milne <bgmilne@mandriva.org> 1.0.32-10mdv2010.1
+ Revision: 490361
- Rebuild for db-4.8

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-9mdv2010.0
+ Revision: 406681
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-8mdv2009.1
+ Revision: 326272
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-7mdv2009.0
+ Revision: 235125
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-6mdv2009.0
+ Revision: 215669
- fix rebuild

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-5mdv2008.1
+ Revision: 182873
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.0.32-4mdv2008.1
+ Revision: 170760
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-3mdv2008.0
+ Revision: 82699
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-2mdv2007.1
+ Revision: 140774
- rebuild

* Wed Mar 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.32-1mdv2007.1
+ Revision: 134884
- 1.0.32

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.30-1mdv2007.0
+ Revision: 79549
- Import apache-mod_vhs

* Sat Jul 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.30-1mdv2007.0
- initial Mandriva package

