from pathlib import Path
import re

import pytest
import frontmatter

profiles_path = Path(__file__).parent.parent / 'web_source' / 'travellers'

travellers = list(profiles_path.glob('*qmd'))
print(profiles_path, travellers)

@pytest.mark.parametrize('traveller', travellers)             
def test_all_profiles(traveller):
    post = frontmatter.load(traveller)
    expected_keys = set(['title', 'subtitle', 'image', 'toc', 'about'])
    assert set(post.keys()) == expected_keys
    assert post['about'] == {'template': 'jolla', 'id': 'person-profile'}

    image = re.compile(r'\.(?:jpg|png)')
    assert image.findall(post['image'])

    breadcrumb = """```{=html}
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="../travellers.html">Travellers</a></li>
    <li class="breadcrumb-item active" aria-current="page">{{< meta title >}}</li>
  </ol>
</nav>
```"""
    assert breadcrumb in post.content, "missing or wrong breadcrumbs"

    profile = """:::{#person-profile}
:::"""
    assert profile in post.content, "missing or wrong profile section"
