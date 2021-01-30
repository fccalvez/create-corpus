import pytest

from parser.wiki_parser import clean_text


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("[[1982]]", ""),
        ("{{Daveoù}}", ""),
        ("[[hi:विकिपीडिया:प्रकाशनाधिकार]]", ""),
        ("([[1982]]-[[1987]])", ""),
        (
            """{{Yezh|anv=Brezhoneg
|broiou=[[Breizh]]
|rannved=[[Europa]]
|komzet= etre 206 000 &lt;ref&gt;TMO 2007&lt;/ref&gt; ha 295 000 &lt;ref&gt;INSEE 2001&lt;/ref&gt;.
|renkadur=goude 100
|livfamilh=Indezeuropek
|familh=[[Yezhoù indezeuropek]]
* [[Yezhoù keltiek]]
**  [[Predeneg]]
*** '''Brezhoneg'''
|YezhOfisiel=
|akademiezh=
|urzh=
|frammadur=
|iso1=br
|iso2=bre 
|lizherennoù=[http://www.sil.org/iso639-3/documentation.asp?id=bre BRE]
}}""",
            "",
        ),
        (
            """<gallery mode"packed" heights"200px">
Yalc'had Skoazell Desk ESPE.jpg Bruderezh evit ar yalc'had Skoazell & Desk
Yalc'had Skoazell Desk.jpg Levrioùgoù evit broudañ studierien da c'houlenn ar yalc'had Skoazell & Desk
</gallery>""",
            "",
        ),
        ("<ref></ref>", ""),
        ("Hervez ur studiadenn bet embannet e 2018 ez eus muioc'h evit 207&nbsp;000 brezhoneger er vro.<ref>[https://www.bretagne.bzh/jcms/prod_435795/fr/etude-sociolinguistique-langues-de-bretagne?detailstrue Bretagne.bzh]</ref>", "Hervez ur studiadenn bet embannet e 2018 ez eus muioc'h evit 207000 brezhoneger er vro."),
        ("([[1987]])", ""),
        ("<!--souezhus :et de l'actuelle région malouine-->", ""),
        ("gwelit [http://ai.ta.free.fr/])", "gwelit )"),
        ("<tt>$1</tt>", ""),
        ("""<gallery mode"packed" heights"300px" style"margin-top
Bicycle evolution-fr.svg Emdroadur ar marc'h-houarn abaoe deroù an XIXvet kantved
1000px-Marc'h-houarn.png Elfennoù pouezusañ ur marc'h-houarn a vremañ
</gallery>""", "")
    ],
)
def test_clean_text(test_input, expected):
    result = clean_text(test_input)

    assert result == expected
