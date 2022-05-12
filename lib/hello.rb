require 'base64'
require 'cgi'
require 'open-uri'
require 'yaml'

group = "哼哼"
hh = {
  "proxies" => [],
  "proxy-groups" => [{
    "name" => group,
    "type" => "select",
    "proxies" => [],
  }],
  "rules" => YAML.safe_load_file(File.join(__dir__, "list.txt")),
}
Base64.decode64(URI(ENV["URL"]).read).each_line do |x|
  if x.chomp.match(/\A([A-Za-z]+):\/\/([A-Za-z0-9+\/=]*)@([A-Za-z0-9.]+):(\d+)#/)
    match = Regexp.last_match
    name = CGI.unescape(match.post_match)
    if name =~ /^「/
      name = "（请选" "择你的干员）"
    else
      name.gsub!(/\A[A-I]/) { ($&.ord - 65).to_s }
      {
        "香港" => "HK",
        "日本" => "JP",
        "新加坡" => "SG",
        "台湾" => "TW",
        "美国" => "US",
        "韩国" => "KR",
        "印度" => "IN",
        "英国" => "UK",
        "阿联酋" => "AE",
        "加拿大" => "CA",
        "澳大利亚" => "AU",
        "瑞士" => "CH",
        "巴西" => "BR",
        "德国" => "DE",
        "俄罗斯" => "RU",
        "莫斯科" => "", "伦敦" => "", "迪拜" => "", "悉尼" => "", "春川" => "",
        "多伦多" => "", "圣保罗" => "",
        "海得拉巴" => "", "法兰克福" => "",
        /\s\p{Han}{2,3}移动/ => " CM",
        /\s\p{Han}{2,3}联通/ => " CU",
        /\s\p{Han}{2,3}电信/ => " CT",
      }.each { |from, to| name.gsub!(from, to) }
      name.strip!
    end
    cipher, password = Base64.decode64(match[2]).split(":")
    hh["proxies"] << {
      "name" => name,
      "type" => match[1],
      "server" => match[3],
      "port" => match[4].to_i,
      "cipher" => cipher,
      "password" => password,
      "udp" => true,
    }
    hh["proxy-groups"][0]["proxies"] << name
  end
end
hh["rules"] << "MATCH,#{group}"
File.write("docs/hello.yml", YAML.dump(hh, header: false).sub(/\A-{3}\n/, ""))
